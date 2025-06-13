"""
Sandbox Manager - Core Docker container management for Python sandboxes.

Handles creation, execution, and cleanup of isolated Python environments
using Docker containers with security restrictions and resource limits.
"""

import uuid
import docker
from typing import Dict, Optional
from datetime import datetime, timedelta
import logging
import docker.models
import docker.models.containers
import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

class SandboxManager:
    """Manages Docker-based Python sandboxes with automatic cleanup and enhanced security."""
    
    def __init__(self, config):
        self.config = config
        self.client = docker.DockerClient(base_url=os.getenv("DOCKER_HOST", "unix://var/run/docker.sock"))
        self.sandboxes: Dict[str, dict] = {}
        self._cleanup_old_sandboxes()  # Clean up on startup
    
    def _cleanup_old_sandboxes(self):
        """Remove sandboxes that haven't been used within timeout period."""
        now = datetime.now()
        to_remove = []
        
        # Find sandboxes that have exceeded timeout
        for sandbox_id, sandbox in self.sandboxes.items():
            if now - sandbox["last_used"] > timedelta(seconds=self.config.sandbox_timeout):
                to_remove.append(sandbox_id)
        
        # Remove expired sandboxes
        for sandbox_id in to_remove:
            self.remove_sandbox(sandbox_id)
    
    def create_sandbox(self) -> str:
        """Create a new isolated Python sandbox container with enhanced security."""
        if len(self.sandboxes) >= self.config.max_sandboxes:
            raise RuntimeError("Maximum number of sandboxes reached")
        
        sandbox_id = str(uuid.uuid4())
        
        try:
            # Create Docker container with enhanced security restrictions
            container = self.client.containers.run(
                self.config.docker_image,
                command=["sleep", "infinity"],  # Safer than string command
                detach=True,
                name=f"omcp-sandbox-{sandbox_id}",
                network_mode="none",      # No network access for security
                mem_limit="512m",         # Memory limit
                cpu_period=100000,        # CPU limits
                cpu_quota=50000,
                remove=True,              # Auto-remove when stopped
                user=1000,       # User isolation
                read_only=True,           # Read-only filesystem
                cap_drop=["ALL"],         # Drop all capabilities
                security_opt=["no-new-privileges"],  # Prevent privilege escalation
                tmpfs={                   # Temporary filesystem mounts
                    "/tmp": "rw,noexec,nosuid,size=100M",
                    "/sandbox": "rw,noexec,nosuid,size=500M"
                }
            )
            
            # Track sandbox metadata
            self.sandboxes[sandbox_id] = {
                "container": container,
                "created_at": datetime.now(),
                "last_used": datetime.now()
            }
            
            logger.info(f"Created new sandbox {sandbox_id}")
            return sandbox_id
            
        except Exception as e:
            logger.error(f"Failed to create sandbox: {e}")
            raise
    
    def remove_sandbox(self, sandbox_id: str):
        """Remove a sandbox container and clean up resources."""
        if sandbox_id not in self.sandboxes:
            return
        
        try:
            # Stop and remove the Docker container
            container:docker.models.containers.Container = self.sandboxes[sandbox_id]["container"]
            container.stop(timeout=1)
            container.remove()
            del self.sandboxes[sandbox_id]
            logger.info(f"Removed sandbox {sandbox_id}")
        except Exception as e:
            logger.error(f"Failed to remove sandbox {sandbox_id}: {e}")
    
    def execute_code(self, sandbox_id: str, code: str) -> docker.models.containers.ExecResult :
        """Execute Python code in the specified sandbox container (legacy method)."""
        if sandbox_id not in self.sandboxes:
            raise ValueError(f"Sandbox {sandbox_id} not found")
        
        container:docker.models.containers.Container = self.sandboxes[sandbox_id]["container"]
        self.sandboxes[sandbox_id]["last_used"] = datetime.now()  # Update usage time
        
        try:
            # Execute code in container and capture output
            exec_result = container.exec_run(
                ["python3", "-c",code]
            )

            return exec_result
        except Exception as e:
            logger.error(f"Failed to execute code in sandbox {sandbox_id}: {e}")
            raise

    def list_sandboxes(self) -> list:
        """Return list of all active sandboxes with metadata."""
        return [
            {
                "id": sandbox_id,
                "created_at": sandbox["created_at"].isoformat(),
                "last_used": sandbox["last_used"].isoformat()
            }
            for sandbox_id, sandbox in self.sandboxes.items()
        ] 