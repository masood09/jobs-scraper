import logging

from flask import Flask, jsonify, request
from jobspy import scrape_jobs
import pandas as pd

from .auth import require_token
from .config import DEBUG_MODE, LOG_FILE_PATH, LOG_LEVEL_VALUE, LOG_TO_FILE


def dataframe_to_serializable_dict(df: pd.DataFrame) -> list:
    """
    Convert DataFrame to JSON-serializable dictionary with proper NaN handling.
    
    Args:
        df: Pandas DataFrame to convert
        
    Returns:
        list: List of dictionaries where NaN values are converted to None
    """
    # Convert DataFrame to dictionary using orient='records'
    jobs_data = df.to_dict(orient="records")
    
    # Process each job to replace NaN/NaT values with None
    processed_jobs = []
    for job in jobs_data:
        processed_job = {}
        for key, value in job.items():
            # Check if value is NaN (float) or NaT (datetime)
            if pd.isna(value):
                processed_job[key] = None
            else:
                processed_job[key] = value
        processed_jobs.append(processed_job)
    
    return processed_jobs


app = Flask(__name__)

# Configure logging
handlers = [logging.StreamHandler()]

if LOG_TO_FILE:
    handlers.append(logging.FileHandler(LOG_FILE_PATH))

logging.basicConfig(
    level=LOG_LEVEL_VALUE,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=handlers,
)
logger = logging.getLogger(__name__)

logger.info(f"Logging configured with level: {logging.getLevelName(LOG_LEVEL_VALUE)}")
logger.info(f"File logging: {LOG_TO_FILE}")
logger.info(f"Debug mode: {DEBUG_MODE}")


@app.route("/scrape", methods=["POST"])
@require_token
def scrape_jobs_endpoint():
    """
    Scrape jobs using the python-jobspy package.
    Accepts POST parameters for scrape_jobs configuration.
    Returns JSON response with job data.
    """
    try:
        # Get parameters from POST request
        data = request.get_json()

        if not data:
            logger.warning("Empty JSON payload received")
            return (
                jsonify(
                    {
                        "error": "Invalid request",
                        "message": "Request body must be JSON with scraping parameters",
                    }
                ),
                400,
            )

        logger.info(f"Received scrape request: {data}")

        # Extract all parameters without any defaults - only pass what's provided
        scrape_params = {}

        # List of all possible parameters
        possible_params = [
            "site_name",
            "search_term",
            "google_search_term",
            "location",
            "results_wanted",
            "hours_old",
            "country_indeed",
            "distance",
            "job_type",
            "proxies",
            "is_remote",
            "easy_apply",
            "user_agent",
            "description_format",
            "offset",
            "verbose",
            "linkedin_fetch_description",
            "linkedin_company_ids",
            "enforce_annual_salary",
            "ca_cert",
        ]

        # Only include parameters that were actually provided
        for param in possible_params:
            if param in data:
                scrape_params[param] = data[param]

        # Debugging: print parameters being passed to scrape_jobs
        logger.debug(f"Scraping parameters: {scrape_params}")

        # Log info about the scrape request
        logger.info(f"Starting job scrape with {len(scrape_params)} parameters")
        if "search_term" in scrape_params:
            logger.info(f"Search term: {scrape_params['search_term']}")
        if "location" in scrape_params:
            logger.info(f"Location: {scrape_params['location']}")

        # Scrape jobs with only the provided parameters
        jobs = scrape_jobs(**scrape_params)

        logger.info(f"Successfully scraped {len(jobs)} jobs")

        # Convert jobs to JSON-serializable format with proper NaN handling
        jobs_data = dataframe_to_serializable_dict(jobs)

        return jsonify({"success": True, "count": len(jobs), "jobs": jobs_data})

    except Exception as e:
        logger.error(f"Failed to scrape jobs: {str(e)}", exc_info=True)

        # Check if this is a JSON parsing error (BadRequest from Flask/Werkzeug)
        if hasattr(e, "code") and e.code == 400:
            return (
                jsonify(
                    {
                        "error": "Invalid request",
                        "message": "Request body must be JSON with scraping parameters",
                    }
                ),
                400,
            )

        return (
            jsonify(
                {"success": False, "error": str(e), "message": "Failed to scrape jobs"}
            ),
            500,
        )


@app.route("/health")
def health_check():
    logger.info("Health check endpoint accessed")
    return "API is running"


@app.before_request
def before_request():
    """Log basic request information"""
    logger.debug(f"Request: {request.method} {request.path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="JobScraper API Server")
    parser.add_argument("--port", type=int, default=8080, help="Port to run on")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind to")
    args = parser.parse_args()

    logger.info(f"Starting Job Scraper API server on {args.host}:{args.port}")

    if DEBUG_MODE:
        logger.info("Running in development mode with Flask debug server")
        app.run(debug=True, host=args.host, port=args.port)
    else:
        logger.info("Running in production mode")
        # This will be handled by Gunicorn when running: gunicorn app:app -b 0.0.0.0:8080 -w 4
        print("\n=== PRODUCTION MODE ===")
        print(f"Run with: gunicorn app:app -b {args.host}:{args.port} -w 4 -k gthread")
        print("Or use: python app.py (with DEBUG_MODE=True for development)")
        print("=======================\n")
