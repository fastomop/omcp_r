"""
OMCP R Sandbox - Secure R Code Execution Environment

A MCP-compliant server for executing R code in isolated Docker containers.
"""

__version__ = "0.1.0"

from omcp_r.config import get_config, RConfig
from omcp_r.sandbox_manager import SessionManager

__all__ = [
    "get_config",
    "RConfig", 
    "SessionManager",
    "__version__",
]
