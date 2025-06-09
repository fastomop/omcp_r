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
import requests

logger = logging.getLogger(__name__)

class SandboxManager:
    """Manages Docker-based Python sandboxes with automatic cleanup and enhanced security."""
    
    def __init__(self, config):
        self.config = config
        self.client = docker.from_env()
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
                user="sandboxuser",       # User isolation
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
            container = self.sandboxes[sandbox_id]["container"]
            container.stop(timeout=1)
            container.remove()
            del self.sandboxes[sandbox_id]
            logger.info(f"Removed sandbox {sandbox_id}")
        except Exception as e:
            logger.error(f"Failed to remove sandbox {sandbox_id}: {e}")
    
    def execute_code(self, sandbox_id: str, code: str) -> dict:
        """Execute Python code in the specified sandbox container (legacy method)."""
        if sandbox_id not in self.sandboxes:
            raise ValueError(f"Sandbox {sandbox_id} not found")
        
        container = self.sandboxes[sandbox_id]["container"]
        self.sandboxes[sandbox_id]["last_used"] = datetime.now()  # Update usage time
        
        try:
            # Execute code in container and capture output
            exec_result = container.exec_run(
                f"python3 -c '{code}'",
                capture_output=True,
                text=True
            )
            
            return {
                "stdout": exec_result.output,
                "stderr": exec_result.stderr,
                "exit_code": exec_result.exit_code
            }
        except Exception as e:
            logger.error(f"Failed to execute code in sandbox {sandbox_id}: {e}")
            raise
    
    def execute_code_secure(self, sandbox_id: str, code: str, timeout: Optional[int] = 30) -> dict:
        """Execute Python code with enhanced security and timeout handling."""
        if sandbox_id not in self.sandboxes:
            raise ValueError(f"Sandbox {sandbox_id} not found")
        
        container = self.sandboxes[sandbox_id]["container"]
        self.sandboxes[sandbox_id]["last_used"] = datetime.now()  # Update usage time
        
        try:
            # Create exec instance with enhanced security
            exec_id = self.client.api.exec_create(
                container.id,
                ["python3", "-c", code],  # List-form command for security
                user="sandboxuser",
                workdir="/sandbox"
            )
            
            # Execute with timeout handling
            try:
                output = self.client.api.exec_start(
                    exec_id,
                    socket=True,
                    timeout=timeout
                )
                
                # Get exec info for exit code
                exec_info = self.client.api.exec_inspect(exec_id)
                exit_code = exec_info.get('ExitCode', 1)
                
                return {
                    "stdout": output.decode('utf-8') if output else "",
                    "stderr": "",  # stderr is captured in stdout for exec_start
                    "exit_code": exit_code
                }
                
            except requests.exceptions.ReadTimeout:
                # Handle timeout specifically
                logger.error(f"Code execution timed out in sandbox {sandbox_id}")
                return {
                    "stdout": "",
                    "stderr": "Code execution timed out",
                    "exit_code": 124  # SIGTERM exit code
                }
                
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