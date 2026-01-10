import uuid
import docker
from typing import Dict, Optional
from datetime import datetime, timedelta
import logging
import docker.models
import docker.models.containers
import os
from dotenv import load_dotenv, find_dotenv
import pyRserve

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
            raise RuntimeError("Maximum number of sessions reached")
        session_id = str(uuid.uuid4())
        try:
            env_vars = {
                "DB_HOST": self.config.db_host,
                "DB_PORT": str(self.config.db_port),
                "DB_USER": self.config.db_user,
                "DB_PASSWORD": self.config.db_password,
                "DB_NAME": self.config.db_name
            }
            # Expose Rserve port (default 6311)
            ports = {'6311/tcp': None}  # Let Docker assign a random host port
            container = self.client.containers.run(
                self.config.docker_image,
                detach=True,
                name=f"omcp-r-session-{session_id}",
                mem_limit="512m",
                cpu_period=100000,
                cpu_quota=50000,
                remove=True,
                user=1000,
                read_only=True,
                cap_drop=["ALL"],
                security_opt=["no-new-privileges"],
                tmpfs={
                    "/tmp": "rw,noexec,nosuid,size=100M",
                    "/sandbox": "rw,noexec,nosuid,size=500M"
                },
                environment=env_vars,
                ports=ports
            )
            # Get the mapped host port for Rserve
            container.reload()
            host_port = container.attrs['NetworkSettings']['Ports']['6311/tcp'][0]['HostPort']
            self.sessions[session_id] = {
                "container": container,
                "created_at": datetime.now(),
                "last_used": datetime.now(),
                "host_port": host_port
            }
            logger.info(f"Created new R session {session_id} (Rserve on port {host_port})")
            return session_id
        except Exception as e:
            logger.error(f"Failed to create R session: {e}")
            raise

    def close_session(self, session_id: str):
        if session_id not in self.sessions:
            return
        try:
            container:docker.models.containers.Container = self.sessions[session_id]["container"]
            container.stop(timeout=1)
            container.remove()
            del self.sessions[session_id]
            logger.info(f"Closed R session {session_id}")
        except Exception as e:
            logger.error(f"Failed to close R session {session_id}: {e}")

    def execute_in_session(self, session_id: str, code: str) -> dict:
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        session = self.sessions[session_id]
        session["last_used"] = datetime.now()
        host = "localhost"
        port = int(session["host_port"])
        try:
            conn = pyRserve.connect(host=host, port=port)
            result = conn.eval(code)
            conn.close()
            return {"success": True, "result": result}
        except Exception as e:
            logger.error(f"Failed to execute R code in session {session_id}: {e}")
            return {"success": False, "error": str(e)}

    def list_files(self, session_id: str, path: str = ".") -> list:
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        container = self.sessions[session_id]["container"]
        # Use ls -F to distinguish directories
        exec_result = container.exec_run(["ls", "-F", path])
        if exec_result.exit_code != 0:
            raise Exception(f"Failed to list files: {exec_result.output.decode()}")
            
        output = exec_result.output.decode()
        files = []
        for line in output.splitlines():
            line = line.strip()
            if not line: continue
            is_dir = line.endswith('/')
            name = line[:-1] if is_dir else line
            files.append({
                "name": name,
                "is_dir": is_dir,
                "path": os.path.join(path, name) if path != "." else name
            })
        return files

    def read_file(self, session_id: str, path: str) -> str:
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
            
        container = self.sessions[session_id]["container"]
        # Use tar to extract file content
        try:
            bits, stat = container.get_archive(path)
            import io
            import tarfile
            
            file_obj = io.BytesIO()
            for chunk in bits:
                file_obj.write(chunk)
            file_obj.seek(0)
            
            with tarfile.open(fileobj=file_obj) as tar:
                # The tar contains the file with its basename
                member = tar.next()
                f = tar.extractfile(member)
                content = f.read().decode('utf-8', errors='replace')
                return content
        except Exception as e:
            raise Exception(f"Failed to read file {path}: {str(e)}")

    def write_file(self, session_id: str, path: str, content: str) -> bool:
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
            
        container = self.sessions[session_id]["container"]
        try:
            # Create a tar archive in memory with the file
            import io
            import tarfile
            import time
            
            dirname = os.path.dirname(path)
            basename = os.path.basename(path)
            
            # If path has directory, ensure it exists
            if dirname and dirname != ".":
                 container.exec_run(["mkdir", "-p", dirname])
            
            data = content.encode('utf-8')
            file_obj = io.BytesIO(data)
            
            tar_stream = io.BytesIO()
            with tarfile.open(fileobj=tar_stream, mode='w') as tar:
                tarinfo = tarfile.TarInfo(name=basename)
                tarinfo.size = len(data)
                tarinfo.mtime = time.time()
                tar.addfile(tarinfo, file_obj)
            
            tar_stream.seek(0)
            
            # Put archive into container
            # If dirname is empty, put in workdir (which is default destination)
            dest = dirname if dirname else "/sandbox"
            
            container.put_archive(dest, tar_stream)
            return True
        except Exception as e:
            raise Exception(f"Failed to write file {path}: {str(e)}")

    def list_sessions(self) -> list:
        return [
            {
                "id": session_id,
                "created_at": session["created_at"].isoformat(),
                "last_used": session["last_used"].isoformat(),
                "host_port": session["host_port"]
            }
            for session_id, session in self.sessions.items()
        ] 