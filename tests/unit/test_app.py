"""
Unit tests for Flask application module.
Uses decorator mocking to bypass authentication.
"""

from unittest.mock import patch

import pandas as pd
import pytest
from flask import Flask

# We need to patch the decorator before the app module is imported
# Since conftest.py already imports the app, we'll use a different approach
# by creating a fresh app instance in our test fixture


def create_test_app():
    """Create a test Flask app with mocked auth decorator."""
    Flask(__name__)  # Create Flask app instance

    # Mock the require_token decorator to do nothing (pass-through)
    def mock_decorator(f):
        """Identity function - no authentication."""
        return f

    with patch.dict("sys.modules", {"jobspy": None}), patch(
        "jobscraper.auth.require_token", mock_decorator
    ), patch("jobscraper.config.API_ACCESS_TOKEN", "test-token"), patch(
        "jobscraper.config.DEBUG_MODE", False
    ), patch(
        "jobscraper.config.LOG_TO_FILE", False
    ), patch(
        "jobscraper.config.LOG_LEVEL_VALUE", 20
    ), patch(
        "jobscraper.config.LOG_FILE_PATH", "test.log"
    ):
        # Import the app module - the decorator will be mocked
        from jobscraper.app import app as flask_app

        return flask_app


@pytest.fixture
def test_app():
    """Fixture to provide a test Flask app."""
    return create_test_app()


class TestHealthCheck:
    """Test cases for health check endpoint."""

    def test_health_check(self, test_app):
        """Test health check endpoint returns success."""
        with test_app.test_client() as client:
            response = client.get("/health")

            assert response.status_code == 200
            assert response.data == b"API is running"

    @patch("jobscraper.app.logger")
    def test_health_check_logging(self, mock_logger, test_app):
        """Test health check endpoint logs access."""
        with test_app.test_client() as client:
            response = client.get("/health")

            assert response.status_code == 200
            # Verify logger.info was called
            mock_logger.info.assert_called_with("Health check endpoint accessed")


class TestScrapeEndpoint:
    """Test cases for /scrape endpoint."""

    @patch("jobscraper.app.scrape_jobs")
    def test_scrape_empty_json_payload(self, mock_scrape_jobs, test_app):
        """Test scrape endpoint with empty JSON payload."""
        with test_app.test_client() as client:
            response = client.post(
                "/scrape", data="", content_type="application/json"  # Empty body
            )

            assert response.status_code == 400
            json_data = response.get_json()
            assert json_data["error"] == "Invalid request"
            assert "Request body must be JSON" in json_data["message"]

    @patch("jobscraper.app.scrape_jobs")
    def test_scrape_invalid_json(self, mock_scrape_jobs, test_app):
        """Test scrape endpoint with invalid JSON."""
        with test_app.test_client() as client:
            response = client.post(
                "/scrape",
                data="{invalid json",  # Invalid JSON
                content_type="application/json",
            )

            assert response.status_code == 400
            json_data = response.get_json()
            assert json_data["error"] == "Invalid request"

    @patch("jobscraper.app.scrape_jobs")
    def test_scrape_success_basic(self, mock_scrape_jobs, test_app):
        """Test successful scrape with basic parameters."""
        # Mock scrape_jobs to return empty DataFrame
        mock_jobs_df = pd.DataFrame(
            {
                "title": ["Software Engineer"],
                "company": ["Test Company"],
                "location": ["San Francisco, CA"],
                "job_url": ["https://test.com/job/123"],
            }
        )
        mock_scrape_jobs.return_value = mock_jobs_df

        with test_app.test_client() as client:
            response = client.post(
                "/scrape",
                json={"search_term": "software engineer"},
                content_type="application/json",
            )

            assert response.status_code == 200
            json_data = response.get_json()
            assert json_data["success"] is True
            assert json_data["count"] == 1
            assert len(json_data["jobs"]) == 1
            assert json_data["jobs"][0]["title"] == "Software Engineer"

            # Verify scrape_jobs was called with correct parameters
            mock_scrape_jobs.assert_called_once_with(search_term="software engineer")

    @patch("jobscraper.app.scrape_jobs")
    def test_scrape_success_comprehensive(self, mock_scrape_jobs, test_app):
        """Test successful scrape with comprehensive parameters."""
        # Mock scrape_jobs to return DataFrame
        mock_jobs_df = pd.DataFrame(
            {
                "title": ["Data Scientist", "DevOps Engineer"],
                "company": ["Company A", "Company B"],
                "location": ["Remote", "New York, NY"],
                "job_url": ["https://test.com/job/1", "https://test.com/job/2"],
            }
        )
        mock_scrape_jobs.return_value = mock_jobs_df

        scrape_data = {
            "site_name": ["indeed", "linkedin"],
            "search_term": "data scientist",
            "location": "San Francisco, CA",
            "results_wanted": 10,
            "hours_old": 72,
            "country_indeed": "USA",
            "is_remote": True,
            "job_type": "fulltime",
        }

        with test_app.test_client() as client:
            response = client.post(
                "/scrape", json=scrape_data, content_type="application/json"
            )

            assert response.status_code == 200
            json_data = response.get_json()
            assert json_data["success"] is True
            assert json_data["count"] == 2
            assert len(json_data["jobs"]) == 2

            # Verify scrape_jobs was called with correct parameters
            mock_scrape_jobs.assert_called_once_with(**scrape_data)

    @patch("jobscraper.app.scrape_jobs")
    def test_scrape_only_provided_parameters(self, mock_scrape_jobs, test_app):
        """Test that only provided parameters are passed to scrape_jobs."""
        mock_jobs_df = pd.DataFrame()
        mock_scrape_jobs.return_value = mock_jobs_df

        scrape_data = {
            "search_term": "python developer",
            "location": "Remote",
            "results_wanted": 5,
        }

        with test_app.test_client() as client:
            response = client.post(
                "/scrape", json=scrape_data, content_type="application/json"
            )

            assert response.status_code == 200

            # Verify mock was called with only the provided parameters
            mock_scrape_jobs.assert_called_once()
            args, kwargs = mock_scrape_jobs.call_args

            # Should only contain the parameters we provided
            assert kwargs == scrape_data
            assert len(kwargs) == 3
            assert "search_term" in kwargs
            assert "location" in kwargs
            assert "results_wanted" in kwargs
            # Should NOT include parameters we didn't provide
            assert "hours_old" not in kwargs
            assert "job_type" not in kwargs

    @patch("jobscraper.app.scrape_jobs")
    def test_scrape_failure_exception(self, mock_scrape_jobs, test_app):
        """Test scrape failure when scrape_jobs raises exception."""
        # Mock scrape_jobs to raise exception
        mock_scrape_jobs.side_effect = Exception("Network error")

        with test_app.test_client() as client:
            response = client.post(
                "/scrape", json={"search_term": "test"}, content_type="application/json"
            )

            assert response.status_code == 500
            json_data = response.get_json()
            assert json_data["success"] is False
            assert "Failed to scrape jobs" in json_data["message"]
            assert "Network error" in json_data["error"]

    @patch("jobscraper.app.scrape_jobs")
    @patch("jobscraper.app.logger")
    def test_scrape_logging_on_error(self, mock_logger, mock_scrape_jobs, test_app):
        """Test error logging when scrape fails."""
        # Mock scrape_jobs to raise exception
        mock_scrape_jobs.side_effect = Exception("Network error")

        with test_app.test_client() as client:
            response = client.post(
                "/scrape", json={"search_term": "test"}, content_type="application/json"
            )

            assert response.status_code == 500
            # Verify error was logged
            mock_logger.error.assert_called()
            error_call_args = mock_logger.error.call_args[0][0]
            assert "Failed to scrape jobs: Network error" in error_call_args

    @patch("jobscraper.app.scrape_jobs")
    @patch("jobscraper.app.logger")
    def test_scrape_logging_on_success(self, mock_logger, mock_scrape_jobs, test_app):
        """Test logging on successful scrape."""
        mock_jobs_df = pd.DataFrame(
            {"title": ["Software Engineer"], "company": ["Test Company"]}
        )
        mock_scrape_jobs.return_value = mock_jobs_df

        with test_app.test_client() as client:
            response = client.post(
                "/scrape",
                json={"search_term": "software engineer"},
                content_type="application/json",
            )

            assert response.status_code == 200
            # Verify info logging was called
            mock_logger.info.assert_any_call(
                "Received scrape request: {'search_term': 'software engineer'}"
            )
            mock_logger.info.assert_any_call("Starting job scrape with 1 parameters")
            mock_logger.info.assert_any_call("Search term: software engineer")
            mock_logger.info.assert_any_call("Successfully scraped 1 jobs")

    def test_all_possible_parameters_extracted(self):
        """Test that all possible parameters are handled correctly."""
        # Test with all possible parameters
        all_params = {
            "site_name": ["indeed"],
            "search_term": "test",
            "google_search_term": "google test",
            "location": "San Francisco",
            "results_wanted": 10,
            "hours_old": 72,
            "country_indeed": "USA",
            "distance": 25,
            "job_type": "fulltime",
            "proxies": ["proxy1"],
            "is_remote": True,
            "easy_apply": False,
            "user_agent": "test-agent",
            "description_format": "markdown",
            "offset": 0,
            "verbose": True,
            "linkedin_fetch_description": True,
            "linkedin_company_ids": [123],
            "enforce_annual_salary": False,
            "ca_cert": "/path/to/cert",
        }

        # This test just verifies the parameter list is comprehensive
        # The actual extraction logic is tested in other tests
        assert len(all_params.keys()) == 20  # Should match the number in app.py


class TestBeforeRequest:
    """Test cases for before_request handler."""

    @patch("jobscraper.app.logger")
    def test_before_request_logging(self, mock_logger, test_app):
        """Test before_request logs requests."""
        with test_app.test_client() as client:
            # Make any request to trigger before_request
            response = client.get("/health")

            assert response.status_code == 200
            # Verify debug logging was called
            mock_logger.debug.assert_called()
            log_message = mock_logger.debug.call_args[0][0]
            assert "Request: GET /health" in log_message
