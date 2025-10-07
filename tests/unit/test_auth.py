"""
Unit tests for authentication module.
"""

from unittest.mock import MagicMock, patch

import pytest
from flask import Flask

# Mock jobspy before importing app modules
with patch.dict("sys.modules", {"jobspy": None}):
    # Create a mock config module
    mock_config = MagicMock()
    mock_config.API_ACCESS_TOKEN = "test-token"

    with patch.dict("sys.modules", {"jobscraper.config": mock_config}):
        from jobscraper.auth import get_required_token, require_token


class TestGetRequiredToken:
    """Test cases for get_required_token function."""

    @patch("jobscraper.auth.API_ACCESS_TOKEN", "test-token")
    def test_get_required_token_valid(self):
        """Test getting a valid token from environment."""
        token = get_required_token()
        assert token == "test-token"

    @patch("jobscraper.auth.API_ACCESS_TOKEN", "default-token-for-development")
    def test_get_required_token_default_token(self):
        """Test getting default development token."""
        with pytest.raises(
            ValueError, match="API_ACCESS_TOKEN is not properly configured"
        ):
            get_required_token()

    @patch("jobscraper.auth.API_ACCESS_TOKEN", "")
    def test_get_required_token_empty_token(self):
        """Test getting empty token from environment."""
        with pytest.raises(
            ValueError, match="API_ACCESS_TOKEN is not properly configured"
        ):
            get_required_token()


class TestRequireTokenDecorator:
    """Test cases for require_token decorator."""

    @pytest.fixture
    def mock_app(self):
        """Create a mock Flask app for testing."""
        app = Flask(__name__)
        return app

    @patch("jobscraper.auth.API_ACCESS_TOKEN", "valid-token")
    def test_require_token_missing_header(self, mock_app):
        """Test decorator with missing Authorization header."""
        with mock_app.test_request_context("/test", method="POST"):

            @require_token
            def test_endpoint():
                return "success"

            result = test_endpoint()
            assert result[1] == 401
            assert "Authorization header required" in result[0].get_json()["error"]

    @patch("jobscraper.auth.API_ACCESS_TOKEN", "valid-token")
    def test_require_token_invalid_format(self, mock_app):
        """Test decorator with invalid Authorization format."""
        headers = {"Authorization": "InvalidFormat token"}
        with mock_app.test_request_context("/test", method="POST", headers=headers):

            @require_token
            def test_endpoint():
                return "success"

            result = test_endpoint()
            assert result[1] == 401
            assert "Invalid authorization format" in result[0].get_json()["error"]

    @patch("jobscraper.auth.API_ACCESS_TOKEN", "valid-token")
    def test_require_token_invalid_token(self, mock_app):
        """Test decorator with invalid token."""
        headers = {"Authorization": "Bearer invalid-token"}
        with mock_app.test_request_context("/test", method="POST", headers=headers):

            @require_token
            def test_endpoint():
                return "success"

            result = test_endpoint()
            assert result[1] == 403
            assert "Invalid access token" in result[0].get_json()["error"]

    @patch("jobscraper.auth.API_ACCESS_TOKEN", "valid-token")
    def test_require_token_valid_token(self, mock_app):
        """Test decorator with valid token."""
        headers = {"Authorization": "Bearer valid-token"}
        with mock_app.test_request_context("/test", method="POST", headers=headers):

            @require_token
            def test_endpoint():
                return "success"

            result = test_endpoint()
            assert result == "success"

    @patch("jobscraper.auth.API_ACCESS_TOKEN", "default-token-for-development")
    def test_require_token_server_config_error(self, mock_app):
        """Test decorator when server token is not configured."""
        headers = {"Authorization": "Bearer any-token"}
        with mock_app.test_request_context("/test", method="POST", headers=headers):

            @require_token
            def test_endpoint():
                return "success"

            result = test_endpoint()
            assert result[1] == 500
            assert "Server configuration error" in result[0].get_json()["error"]
