from __future__ import annotations

import io
import logging
import os
import tarfile
import time
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import docker
import docker.models
import docker.models.containers
import pyRserve
from dotenv import find_dotenv, load_dotenv

from omcp_r.errors import SandboxError
from omcp_r.execution_limits import ExecutionLimits
from omcp_r.path_policy import SANDBOX_ROOT, normalize_session_path, to_user_path

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

class SessionManager:
    """Manages persistent R sessions (Docker containers running Rserve) with automatic cleanup and enhanced security."""

    def __init__(self, config):
        self.config = config
        self.client = docker.DockerClient(base_url=os.getenv("DOCKER_HOST", "unix://var/run/docker.sock"))
        self.sessions: Dict[str, dict] = {}
        self._cleanup_old_sessions()

    def _cleanup_old_sessions(self):
        now = datetime.now()
        to_remove = []
        for session_id, session in self.sessions.items():
            if now - session["last_used"] > timedelta(seconds=self.config.sandbox_timeout):
                to_remove.append(session_id)
        for session_id in to_remove:
            self.close_session(session_id)

    def create_session(self) -> str:
        if len(self.sessions) >= self.config.max_sandboxes:
            raise SandboxError("max_sessions_reached", "Maximum number of sessions reached")
        session_id = str(uuid.uuid4())
        try:
            # Database Proxying: Replace localhost with host.docker.internal
            db_host = self.config.db_host
            extra_hosts = {}
            if db_host in ["localhost", "127.0.0.1"]:
                db_host = "host.docker.internal"
                extra_hosts = {"host.docker.internal": "host-gateway"}

            env_vars = {
                "DB_HOST": db_host,
                "DB_PORT": str(self.config.db_port),
                "DB_USER": self.config.db_user,
                "DB_PASSWORD": self.config.db_password,
                "DB_NAME": self.config.db_name,
            }

            # Persistent Workspace
            volumes = {}
            if self.config.workspace_root:
                session_dir = os.path.join(self.config.workspace_root, session_id)
                os.makedirs(session_dir, exist_ok=True)
                # Mount as R/W
                volumes[session_dir] = {"bind": SANDBOX_ROOT, "mode": "rw"}

            # Expose Rserve port (default 6311)
            ports = {"6311/tcp": None}  # Let Docker assign a random host port
            container = self.client.containers.run(
                self.config.docker_image,
                detach=True,
                name=f"omcp-r-session-{session_id}",
                mem_limit="512m",
                cpu_period=100000,
                cpu_quota=50000,
                remove=True,
                user=1000,  # sandboxuser
                read_only=True,
                cap_drop=["ALL"],
                security_opt=["no-new-privileges"],
                tmpfs={
                    "/tmp": "rw,noexec,nosuid,size=100M",
                    # only mount /sandbox as tmpfs if NO workspace_volume is used
                    **({SANDBOX_ROOT: "rw,noexec,nosuid,size=500M"} if not volumes else {}),
                },
                environment=env_vars,
                ports=ports,
                volumes=volumes,
                extra_hosts=extra_hosts,
            )
            # Get the mapped host port for Rserve
            container.reload()
            host_port = container.attrs["NetworkSettings"]["Ports"]["6311/tcp"][0]["HostPort"]
            self.sessions[session_id] = {
                "container": container,
                "created_at": datetime.now(),
                "last_used": datetime.now(),
                "host_port": host_port,
                "journal": [],
            }
            logger.info(f"Created new R session {session_id} (Rserve on port {host_port})")
            return session_id
        except SandboxError:
            raise
        except Exception as e:
            logger.error(f"Failed to create R session: {e}")
            raise SandboxError("session_create_failed", "Failed to create R session", retryable=True)

    def close_session(self, session_id: str):
        if session_id not in self.sessions:
            raise SandboxError("session_not_found", f"Session {session_id} not found")
        try:
            container: docker.models.containers.Container = self.sessions[session_id]["container"]
            container.stop(timeout=1)
            container.remove()
            del self.sessions[session_id]
            logger.info(f"Closed R session {session_id}")
        except Exception as e:
            logger.error(f"Failed to close R session {session_id}: {e}")
            raise SandboxError("session_close_failed", f"Failed to close session {session_id}", retryable=True)

    def _require_session(self, session_id: str) -> Dict[str, Any]:
        session = self.sessions.get(session_id)
        if session is None:
            raise SandboxError("session_not_found", f"Session {session_id} not found")
        session["last_used"] = datetime.now()
        return session

    def _truncate_output(self, output: str, max_output_bytes: int) -> tuple[str, bool]:
        encoded = output.encode("utf-8", errors="replace")
        if len(encoded) <= max_output_bytes:
            return output, False
        truncated = encoded[:max_output_bytes].decode("utf-8", errors="ignore")
        return truncated, True

    def execute_in_session(
        self,
        session_id: str,
        code: str,
        limits_payload: Optional[Dict[str, Any]] = None,
    ) -> dict:
        if not isinstance(code, str) or not code.strip():
            raise SandboxError("invalid_code", "code must be a non-empty string")
        if len(code) > self.config.max_code_chars:
            raise SandboxError(
                "code_too_large",
                "code exceeds max allowed size",
                details={"max_code_chars": self.config.max_code_chars},
            )

        limits = ExecutionLimits.from_payload(
            limits_payload,
            default_duration_secs=self.config.default_exec_timeout_secs,
            default_output_bytes=self.config.max_output_bytes,
        )

        session = self._require_session(session_id)
        host = "localhost"
        port = int(session["host_port"])

        # Wrap code to capture output (stdout/stderr) and exception handling
        wrapped_code = f"""
        execution_error <- NULL
        result <- NULL
        output_con <- textConnection("captured_output", "w", local = TRUE)
        start_time <- Sys.time()
        sink(output_con)
        sink(output_con, type = "message")
        setTimeLimit(elapsed = {limits.max_duration_secs}, transient = TRUE)
        tryCatch({{
            result <- {{
                {code}
            }}
        }}, error = function(e) {{
            execution_error <<- conditionMessage(e)
        }}, finally = {{
            setTimeLimit(cpu = Inf, elapsed = Inf, transient = FALSE)
            sink(type = "message")
            sink()
            close(output_con)
        }})
        elapsed_secs <- as.numeric(difftime(Sys.time(), start_time, units = "secs"))
        list(
            output = paste(captured_output, collapse = "\\n"),
            result = result,
            error = execution_error,
            elapsed_secs = elapsed_secs
        )
        """

        try:
            conn = pyRserve.connect(host=host, port=port)
            try:
                eval_res = conn.eval(wrapped_code)
            finally:
                conn.close()

            output_log = str(eval_res.get("output", "")) if hasattr(eval_res, "get") else ""
            output_log, output_truncated = self._truncate_output(output_log, limits.max_output_bytes)
            result_val = eval_res.get("result") if hasattr(eval_res, "get") else None
            error_text = eval_res.get("error") if hasattr(eval_res, "get") else None
            elapsed_secs = float(eval_res.get("elapsed_secs", 0.0)) if hasattr(eval_res, "get") else 0.0

            if error_text:
                code_name = "execution_timeout" if "elapsed time limit" in str(error_text).lower() else "execution_error"
                session["journal"].append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "success": False,
                        "elapsed_secs": elapsed_secs,
                        "code_len": len(code),
                    }
                )
                return {
                    "success": False,
                    "error": {
                        "code": code_name,
                        "message": str(error_text),
                        "retryable": False,
                    },
                    "output": output_log,
                    "meta": {
                        "elapsed_secs": elapsed_secs,
                        "output_truncated": output_truncated,
                    },
                }

            session["journal"].append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "success": True,
                    "elapsed_secs": elapsed_secs,
                    "code_len": len(code),
                }
            )
            return {
                "success": True,
                "result": str(result_val) if result_val is not None else "",
                "output": output_log,
                "meta": {
                    "elapsed_secs": elapsed_secs,
                    "output_truncated": output_truncated,
                },
            }
        except SandboxError:
            raise
        except Exception as e:
            logger.error(f"Failed to execute R code in session {session_id}: {e}")
            raise SandboxError(
                "execution_transport_error",
                "Failed to execute code in R session",
                retryable=True,
                details={"reason": str(e)},
            )

    def list_files(self, session_id: str, path: str = ".") -> list:
        session = self._require_session(session_id)
        try:
            resolved_path = normalize_session_path(path)
        except ValueError as e:
            raise SandboxError("invalid_path", str(e))

        container = session["container"]
        exec_result = container.exec_run(["ls", "-F", resolved_path])
        if exec_result.exit_code != 0:
            raise SandboxError("list_files_failed", exec_result.output.decode(errors="replace").strip())

        output = exec_result.output.decode(errors="replace")
        files = []
        parent = to_user_path(resolved_path)
        for line in output.splitlines():
            line = line.strip()
            if not line:
                continue
            is_dir = line.endswith("/")
            name = line[:-1] if is_dir else line
            relative_path = name if parent in (".", "") else f"{parent}/{name}"
            files.append({"name": name, "is_dir": is_dir, "path": relative_path})
        return files

    def read_file(self, session_id: str, path: str) -> str:
        session = self._require_session(session_id)
        try:
            resolved_path = normalize_session_path(path)
        except ValueError as e:
            raise SandboxError("invalid_path", str(e))

        container = session["container"]
        try:
            bits, _ = container.get_archive(resolved_path)
            file_obj = io.BytesIO()
            for chunk in bits:
                file_obj.write(chunk)
            file_obj.seek(0)

            with tarfile.open(fileobj=file_obj) as tar:
                member = tar.next()
                if member is None:
                    raise SandboxError("read_file_failed", "archive did not contain a file")
                if member.size > self.config.max_file_read_bytes:
                    raise SandboxError(
                        "file_too_large",
                        "file exceeds max read size",
                        details={"max_file_read_bytes": self.config.max_file_read_bytes},
                    )
                f = tar.extractfile(member)
                if f is None:
                    raise SandboxError("read_file_failed", "failed to extract file from archive")
                return f.read().decode("utf-8", errors="replace")
        except SandboxError:
            raise
        except Exception as e:
            raise SandboxError("read_file_failed", f"Failed to read file {path}: {str(e)}")

    def write_file(self, session_id: str, path: str, content: str) -> bool:
        session = self._require_session(session_id)
        try:
            resolved_path = normalize_session_path(path)
        except ValueError as e:
            raise SandboxError("invalid_path", str(e))

        if not isinstance(content, str):
            raise SandboxError("invalid_content", "content must be a string")
        data = content.encode("utf-8")
        if len(data) > self.config.max_file_write_bytes:
            raise SandboxError(
                "file_too_large",
                "content exceeds max write size",
                details={"max_file_write_bytes": self.config.max_file_write_bytes},
            )

        container = session["container"]
        try:
            dirname = os.path.dirname(resolved_path)
            basename = os.path.basename(resolved_path)

            if dirname and dirname != ".":
                container.exec_run(["mkdir", "-p", dirname])

            file_obj = io.BytesIO(data)
            tar_stream = io.BytesIO()
            with tarfile.open(fileobj=tar_stream, mode="w") as tar:
                tarinfo = tarfile.TarInfo(name=basename)
                tarinfo.size = len(data)
                tarinfo.mtime = time.time()
                tar.addfile(tarinfo, file_obj)

            tar_stream.seek(0)
            dest = dirname if dirname else SANDBOX_ROOT
            container.put_archive(dest, tar_stream)
            return True
        except Exception as e:
            raise SandboxError("write_file_failed", f"Failed to write file {path}: {str(e)}")

    def list_sessions(self) -> list:
        return [
            {
                "id": session_id,
                "created_at": session["created_at"].isoformat(),
                "last_used": session["last_used"].isoformat(),
                "host_port": session["host_port"],
                "history_count": len(session.get("journal", [])),
            }
            for session_id, session in self.sessions.items()
        ]
