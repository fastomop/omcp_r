import os
import logging
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class RConfig:
    def __init__(self):
        self.sandbox_timeout = int(os.getenv("SANDBOX_TIMEOUT", 300))
        self.max_sandboxes = int(os.getenv("MAX_SANDBOXES", 10))
        self.docker_image = os.getenv("DOCKER_IMAGE", "omcp-r-sandbox:latest")
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        # Database connection defaults
        self.db_host = os.getenv("DB_HOST", "")
        self.db_port = int(os.getenv("DB_PORT", 5432))
        self.db_user = os.getenv("DB_USER", "")
        self.db_password = os.getenv("DB_PASSWORD", "")
        self.db_name = os.getenv("DB_NAME", "")


def get_config():
    return RConfig() 