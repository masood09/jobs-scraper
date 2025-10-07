# Running the JobScraper API

This document explains how to run the JobScraper API in different modes.

## Installation

### Development Environment
```bash
pip install -r requirements/requirements.dev.txt
```
*Includes core application dependencies plus development tools (testing, linting, formatting)*

### Production Environment
```bash
pip install -r requirements/requirements.prod.txt
```
*Includes core application dependencies plus production server (gunicorn)*

### Core Dependencies Only
```bash
pip install -r requirements/requirements.base.txt
```
*Only the essential application dependencies without dev/prod extras*

## Development Mode (Recommended for development)

Uses Flask's built-in development server with auto-reload and debug features.

### Using run script:
```bash
python scripts/run.py dev
```

### Manual method:
```bash
export DEBUG_MODE=True
export LOG_LEVEL=DEBUG
python -m src.jobscraper
```

**Features:**
- Auto-reload on code changes
- Debug mode enabled
- Detailed error pages
- Development-oriented logging

## Production Mode

Uses Gunicorn WSGI server for production deployment.

### Using run script:
```bash
python scripts/run.py prod
```

### Manual method:
```bash
export DEBUG_MODE=False
export LOG_LEVEL=INFO
gunicorn src.jobscraper.app:app -c config/gunicorn.conf.py
```

**Features:**
- Multiple worker processes
- Production-optimized configuration
- Better performance and stability
- Production logging

## Environment Variables

### Debug Mode Control:
- `DEBUG_MODE=True` - Use Flask development server
- `DEBUG_MODE=False` - Use Gunicorn production server

### Logging Control:
- `LOG_LEVEL=DEBUG` - Detailed debugging logs
- `LOG_LEVEL=INFO` - General operational logs  
- `LOG_LEVEL=WARNING` - Only warnings and errors
- `LOG_LEVEL=ERROR` - Only errors

## Gunicorn Configuration

The `gunicorn.conf.py` file contains production-optimized settings:
- Worker processes based on CPU cores
- Thread-based worker class
- Proper logging configuration
- Timeout and keepalive settings

## Quick Start Examples

### Development:
```bash
# Simple way
export DEBUG_MODE=True && python -m src.jobscraper

# Using run script
python scripts/run.py dev
```

### Production:
```bash
# Simple way
export DEBUG_MODE=False && gunicorn src.jobscraper.app:app -b 0.0.0.0:8080 -w 4

# Using configuration file
gunicorn src.jobscraper.app:app -c config/gunicorn.conf.py

# Using run script
python scripts/run.py prod
```

## Port & Host Configuration

The application runs on port 8080 and localhost (127.0.0.1) by default. To change:

```bash
# For Flask development server (custom port and host)
python -m src.jobscraper --port 9000 --host 0.0.0.0

# For Gunicorn (custom port)
gunicorn src.jobscraper.app:app -b 0.0.0.0:9000 -c config/gunicorn.conf.py

# For external access, bind to 0.0.0.0
gunicorn src.jobscraper.app:app -b 0.0.0.0:8080 -c config/gunicorn.conf.py
```

## Notes

- Always set `DEBUG_MODE=False` in production environments
- Use the run script for consistent behavior across environments
- Gunicorn provides better performance and stability for production use
- Flask development server is ideal for debugging and development
- **macOS Users**: The run script sets `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` to avoid fork() issues
