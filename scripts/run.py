#!/usr/bin/env python3
"""
Run script for JobScraper API.
Use this script to start the application in different modes.
"""

import os
import subprocess
import sys


def run_development():
    """Run in development mode with Flask debug server"""
    print("Starting in development mode...")
    os.environ["DEBUG_MODE"] = "True"
    os.environ["LOG_LEVEL"] = "DEBUG"
    
    # Run the package directly
    os.execvp("python", ["python", "-m", "src.jobscraper", "--port", "8080", "--host", "127.0.0.1"])


def run_production():
    """Run in production mode with Gunicorn"""
    print("Starting in production mode with Gunicorn...")
    os.environ["DEBUG_MODE"] = "False"
    os.environ["LOG_LEVEL"] = "INFO"

    # Set environment variable to disable fork safety check (macOS fix)
    os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"

    # Use Gunicorn with the new package structure
    subprocess.run(
        [
            "gunicorn",
            "src.jobscraper.app:app",
            "--bind",
            "0.0.0.0:8080",
            "--workers",
            "1",
            "--worker-class",
            "sync",
            "--timeout",
            "30",
            "--access-logfile",
            "-",
            "--error-logfile",
            "-",
        ]
    )


def print_usage():
    """Print usage information"""
    print("Usage:")
    print("  python run.py dev     - Run in development mode")
    print("  python run.py prod    - Run in production mode")
    print("  python run.py help    - Show this help")
    print("")
    print("Alternatively:")
    print("  python -m src.jobscraper - Run the package directly")
    print("  gunicorn src.jobscraper.app:app - Run production server")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "dev":
        run_development()
    elif mode == "prod":
        run_production()
    elif mode == "help":
        print_usage()
    else:
        print(f"Unknown mode: {mode}")
        print_usage()
        sys.exit(1)
