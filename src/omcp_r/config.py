import os
import logging
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class RConfig:
    def __init__(self):
        self.sandbox_timeout = int(os.getenv("SANDBOX_TIMEOUT", 300))
        self.max_sandboxes = int(os.getenv("MAX_SANDBOXES", 10))
        self.docker_image = os.getenv("DOCKER_IMAGE", "rocker/r-ver:latest")
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()


def get_config():
    return RConfig() 