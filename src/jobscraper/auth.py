"""
Authentication module for API token validation.
Uses environment variable for token configuration.
"""

import logging
from functools import wraps

from flask import jsonify, request

from .config import API_ACCESS_TOKEN

# Configure logger for auth module
auth_logger = logging.getLogger(__name__)


def get_required_token():
    """
    Get the required token from configuration.
    Returns the token value or raises ValueError if not set.
    """
    if not API_ACCESS_TOKEN or API_ACCESS_TOKEN == "default-token-for-development":
        auth_logger.error("API_ACCESS_TOKEN is not properly configured")
        raise ValueError("API_ACCESS_TOKEN is not properly configured")
    return API_ACCESS_TOKEN


def require_token(f):
    """
    Decorator to require valid access token for API endpoints.
    Only allows access if the provided token matches the environment variable.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            required_token = get_required_token()
            auth_logger.debug(
                "Successfully retrieved API access token from configuration"
            )
        except ValueError:
            auth_logger.error(
                "Server configuration error - API access token not configured"
            )
            return (
                jsonify(
                    {
                        "error": "Server configuration error",
                        "message": "API access token is not configured",
                    }
                ),
                500,
            )

        # Get the Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            auth_logger.warning("Authorization header missing from request")
            return (
                jsonify(
                    {
                        "error": "Authorization header required",
                        "message": "Please provide an access token in the Authorization header",
                    }
                ),
                401,
            )

        # Check if header is in Bearer format
        if not auth_header.startswith("Bearer "):
            auth_logger.warning(f"Invalid authorization format: {auth_header}")
            return (
                jsonify(
                    {
                        "error": "Invalid authorization format",
                        "message": "Authorization header should be in format: Bearer <token>",
                    }
                ),
                401,
            )

        # Extract the token
        provided_token = auth_header[7:]  # Remove 'Bearer ' prefix
        auth_logger.debug("Extracted token from Authorization header")

        # Validate the token (simple string comparison)
        if provided_token != required_token:
            auth_logger.warning("Invalid access token provided")
            return (
                jsonify(
                    {
                        "error": "Invalid access token",
                        "message": "The provided access token is not valid",
                    }
                ),
                403,
            )

        auth_logger.info("Access token validated successfully")
        # Token is valid, proceed with the request
        return f(*args, **kwargs)

    return decorated_function
