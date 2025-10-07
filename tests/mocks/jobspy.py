"""
Mock jobspy module for testing.
"""
import pandas as pd


def scrape_jobs(**kwargs):
    """Mock scrape_jobs function."""
    # Return empty DataFrame for testing
    return pd.DataFrame()
