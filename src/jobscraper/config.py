"""
Configuration file for API settings.
In production, use environment variables or a proper config management solution.
"""

import os

# API Access Token - set this via environment variable
# export API_ACCESS_TOKEN="your-secret-token-here"
API_ACCESS_TOKEN = os.environ.get("API_ACCESS_TOKEN", "default-token-for-development")

# Logging Configuration
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_TO_FILE = os.environ.get("LOG_TO_FILE", "False").lower() == "true"
LOG_FILE_PATH = os.environ.get("LOG_FILE_PATH", "app.log")
DEBUG_MODE = os.environ.get("DEBUG_MODE", "False").lower() == "true"

# Convert string log level to logging constant
if LOG_LEVEL == "DEBUG":
    LOG_LEVEL_VALUE = 10
elif LOG_LEVEL == "INFO":
    LOG_LEVEL_VALUE = 20
elif LOG_LEVEL == "WARNING":
    LOG_LEVEL_VALUE = 30
elif LOG_LEVEL == "ERROR":
    LOG_LEVEL_VALUE = 40
else:
    LOG_LEVEL_VALUE = 20  # Default to INFO

# You can add other configuration settings here as needed
