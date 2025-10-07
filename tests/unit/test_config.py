"""
Unit tests for configuration module.
"""

import os
from unittest.mock import patch

import pytest

# Mock jobspy before importing app modules
with patch.dict("sys.modules", {"jobspy": None}):
    # Import the config module directly instead of individual symbols
    pass


class TestConfig:
    """Test cases for configuration module."""

    def test_api_access_token_default(self):
        """Test API_ACCESS_TOKEN default value."""
        # Remove API_ACCESS_TOKEN from environment to test default
        original_token = os.environ.get("API_ACCESS_TOKEN")
        if "API_ACCESS_TOKEN" in os.environ:
            del os.environ["API_ACCESS_TOKEN"]

        # Re-import to get fresh default value
        import importlib

        import jobscraper.config

        importlib.reload(jobscraper.config)

        assert jobscraper.config.API_ACCESS_TOKEN == "default-token-for-development"

        # Restore environment
        if original_token:
            os.environ["API_ACCESS_TOKEN"] = original_token

    def test_api_access_token_from_env(self):
        """Test API_ACCESS_TOKEN from environment variable."""
        test_token = "test-token-from-env"
        with pytest.MonkeyPatch().context() as m:
            m.setenv("API_ACCESS_TOKEN", test_token)
            # Re-import to get fresh value
            import importlib

            import jobscraper.config

            importlib.reload(jobscraper.config)

            assert jobscraper.config.API_ACCESS_TOKEN == test_token

    def test_log_level_values(self):
        """Test LOG_LEVEL_VALUE conversion."""
        test_cases = [
            ("DEBUG", 10),
            ("INFO", 20),
            ("WARNING", 30),
            ("ERROR", 40),
            ("INVALID", 20),  # Defaults to INFO
        ]

        for level_str, expected_value in test_cases:
            with pytest.MonkeyPatch().context() as m:
                m.setenv("LOG_LEVEL", level_str)
                # Re-import to get fresh value
                import importlib

                import jobscraper.config

                importlib.reload(jobscraper.config)

                assert jobscraper.config.LOG_LEVEL_VALUE == expected_value

    def test_log_to_file_conversion(self):
        """Test LOG_TO_FILE boolean conversion."""
        test_cases = [
            ("True", True),
            ("true", True),
            ("False", False),
            ("false", False),
            ("invalid", False),  # Defaults to False
        ]

        for value_str, expected_bool in test_cases:
            with pytest.MonkeyPatch().context() as m:
                m.setenv("LOG_TO_FILE", value_str)
                # Re-import to get fresh value
                import importlib

                import jobscraper.config

                importlib.reload(jobscraper.config)

                assert jobscraper.config.LOG_TO_FILE == expected_bool

    def test_debug_mode_conversion(self):
        """Test DEBUG_MODE boolean conversion."""
        test_cases = [
            ("True", True),
            ("true", True),
            ("False", False),
            ("false", False),
            ("invalid", False),  # Defaults to False
        ]

        for value_str, expected_bool in test_cases:
            with pytest.MonkeyPatch().context() as m:
                m.setenv("DEBUG_MODE", value_str)
                # Re-import to get fresh value
                import importlib

                import jobscraper.config

                importlib.reload(jobscraper.config)

                assert jobscraper.config.DEBUG_MODE == expected_bool

    def test_log_file_path_default(self):
        """Test LOG_FILE_PATH default value."""
        # Remove LOG_FILE_PATH from environment
        original_path = os.environ.get("LOG_FILE_PATH")
        if "LOG_FILE_PATH" in os.environ:
            del os.environ["LOG_FILE_PATH"]

        # Re-import to get fresh default value
        import importlib

        import jobscraper.config

        importlib.reload(jobscraper.config)

        assert jobscraper.config.LOG_FILE_PATH == "app.log"

        # Restore environment
        if original_path:
            os.environ["LOG_FILE_PATH"] = original_path

    def test_log_file_path_from_env(self):
        """Test LOG_FILE_PATH from environment variable."""
        test_path = "/custom/path/app.log"
        with pytest.MonkeyPatch().context() as m:
            m.setenv("LOG_FILE_PATH", test_path)
            # Re-import to get fresh value
            import importlib

            import jobscraper.config

            importlib.reload(jobscraper.config)

            assert jobscraper.config.LOG_FILE_PATH == test_path
