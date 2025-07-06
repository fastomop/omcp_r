import uuid
import docker
from typing import Dict, Optional
from datetime import datetime, timedelta
import logging
import docker.models
import docker.models.containers
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

class SandboxManager:
    """Manages Docker-based R sandboxes with automatic cleanup and enhanced security."""
    
    def __init__(self, config):
        self.config = config
        self.client = docker.DockerClient(base_url=os.getenv("DOCKER_HOST", "unix://var/run/docker.sock"))
        self.sandboxes: Dict[str, dict] = {}
        self._cleanup_old_sandboxes()  # Clean up on startup
    
    def _cleanup_old_sandboxes(self):
        now = datetime.now()
        to_remove = []
        for sandbox_id, sandbox in self.sandboxes.items():
            if now - sandbox["last_used"] > timedelta(seconds=self.config.sandbox_timeout):
                to_remove.append(sandbox_id)
        for sandbox_id in to_remove:
            self.remove_sandbox(sandbox_id)
    
    def create_sandbox(self) -> str:
        if len(self.sandboxes) >= self.config.max_sandboxes:
            raise RuntimeError("Maximum number of sandboxes reached")
        sandbox_id = str(uuid.uuid4())
        try:
            container = self.client.containers.run(
                self.config.docker_image,
                command=["sleep", "infinity"],
                detach=True,
                name=f"omcp-r-sandbox-{sandbox_id}",
                network_mode="none",
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
                }
            )
            self.sandboxes[sandbox_id] = {
                "container": container,
                "created_at": datetime.now(),
                "last_used": datetime.now()
            }
            logger.info(f"Created new R sandbox {sandbox_id}")
            return sandbox_id
        except Exception as e:
            logger.error(f"Failed to create R sandbox: {e}")
            raise
    
    def remove_sandbox(self, sandbox_id: str):
        if sandbox_id not in self.sandboxes:
            return
        try:
            container:docker.models.containers.Container = self.sandboxes[sandbox_id]["container"]
            container.stop(timeout=1)
            container.remove()
            del self.sandboxes[sandbox_id]
            logger.info(f"Removed R sandbox {sandbox_id}")
        except Exception as e:
            logger.error(f"Failed to remove R sandbox {sandbox_id}: {e}")
    
    def execute_code(self, sandbox_id: str, code: str) -> docker.models.containers.ExecResult:
        if sandbox_id not in self.sandboxes:
            raise ValueError(f"Sandbox {sandbox_id} not found")
        container:docker.models.containers.Container = self.sandboxes[sandbox_id]["container"]
        self.sandboxes[sandbox_id]["last_used"] = datetime.now()
        try:
            exec_result = container.exec_run([
                "Rscript", "-e", code
            ])
            return exec_result
        except Exception as e:
            logger.error(f"Failed to execute R code in sandbox {sandbox_id}: {e}")
            raise

    def list_sandboxes(self) -> list:
        return [
            {
                "id": sandbox_id,
                "created_at": sandbox["created_at"].isoformat(),
                "last_used": sandbox["last_used"].isoformat()
            }
            for sandbox_id, sandbox in self.sandboxes.items()
        ] 