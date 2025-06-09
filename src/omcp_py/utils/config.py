"""
Configuration management for the MCP sandbox server.

Loads configuration from environment variables with sensible defaults
for sandbox timeouts, limits, and logging settings.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

@dataclass
class SandboxConfig:
    """Configuration settings for sandbox behavior and limits."""
    sandbox_timeout: int = 300      # 5 minutes default timeout
    max_sandboxes: int = 10         # Maximum concurrent sandboxes
    docker_image: str = "python:3.11-slim"  # Base Docker image
    sandbox_base_url: Optional[str] = None  # For future HTTP endpoints
    debug: bool = False             # Debug mode flag
    log_level: str = "INFO"         # Logging level

def get_config() -> SandboxConfig:
    """Load and return configuration from environment variables."""
    return SandboxConfig(
        sandbox_timeout=int(os.getenv("SANDBOX_TIMEOUT", "300")),
        max_sandboxes=int(os.getenv("MAX_SANDBOXES", "10")),
        docker_image=os.getenv("DOCKER_IMAGE", "python:3.11-slim"),
        sandbox_base_url=os.getenv("SANDBOX_BASE_URL"),
        debug=os.getenv("DEBUG", "false").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "INFO")
    )
