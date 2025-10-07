"""
Test configuration and fixtures for JobScraper API tests.
"""

import os
import sys
from unittest.mock import patch

import pytest
import werkzeug

# Add src and mocks to Python path
sys.path.insert(0, "src")
sys.path.insert(0, "tests/mocks")

# Workaround for werkzeug version compatibility
if not hasattr(werkzeug, "__version__"):
    # Try to set a version attribute for compatibility
    try:
        import importlib.metadata

        werkzeug.__version__ = importlib.metadata.version("werkzeug")
    except (ImportError, importlib.metadata.PackageNotFoundError):
        # Fallback to a default version
        werkzeug.__version__ = "2.3.0"

# Import app after setting up mocks
# Patch the require_token decorator before importing to avoid import-time execution


def mock_decorator(f):
    """Identity function - no authentication."""
    return f


with patch("jobscraper.auth.require_token", mock_decorator):
    from jobscraper.app import app as flask_app


@pytest.fixture
def app():
    """Provide Flask application for testing."""
    return flask_app


@pytest.fixture
def client(app):
    """Provide test client for Flask application."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Provide CLI runner for Flask application."""
    return app.test_cli_runner()


@pytest.fixture
def mock_scrape_jobs():
    """Mock the jobspy.scrape_jobs function."""
    with patch("jobscraper.app.scrape_jobs") as mock:
        yield mock


@pytest.fixture
def valid_token():
    """Provide a valid API token for testing."""
    return "test-valid-token"


@pytest.fixture
def invalid_token():
    """Provide an invalid API token for testing."""
    return "test-invalid-token"


@pytest.fixture
def set_valid_token_env():
    """Set valid API token environment variable."""
    original_token = os.environ.get("API_ACCESS_TOKEN")
    os.environ["API_ACCESS_TOKEN"] = "test-valid-token"
    yield
    # Restore original environment
    if original_token is not None:
        os.environ["API_ACCESS_TOKEN"] = original_token
    else:
        del os.environ["API_ACCESS_TOKEN"]


@pytest.fixture
def unset_token_env():
    """Unset API token environment variable."""
    original_token = os.environ.get("API_ACCESS_TOKEN")
    if "API_ACCESS_TOKEN" in os.environ:
        del os.environ["API_ACCESS_TOKEN"]
    yield
    # Restore original environment
    if original_token is not None:
        os.environ["API_ACCESS_TOKEN"] = original_token
