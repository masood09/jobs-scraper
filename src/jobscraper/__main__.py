"""
Main entry point for the JobScraper API.
"""

import argparse

from .app import app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JobScraper API Server")
    parser.add_argument("--port", type=int, default=8080, help="Port to run on")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind to")
    args = parser.parse_args()

    app.run(debug=True, host=args.host, port=args.port)
