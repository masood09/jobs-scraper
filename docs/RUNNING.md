# Running the JobScraper API

This document explains how to run the JobScraper API in different modes.

## Development Mode (Recommended for development)

Uses Flask's built-in development server with auto-reload and debug features.

### Using run script:
```bash
python run.py dev
```

### Manual method:
```bash
export DEBUG_MODE=True
export LOG_LEVEL=DEBUG
python app.py
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
python run.py prod
```

### Manual method:
```bash
export DEBUG_MODE=False
export LOG_LEVEL=INFO
gunicorn app:app -c gunicorn.conf.py
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
export DEBUG_MODE=True && python app.py

# Using run script
python run.py dev
```

### Production:
```bash
# Simple way
export DEBUG_MODE=False && gunicorn app:app -b 0.0.0.0:8080 -w 4

# Using configuration file
gunicorn app:app -c gunicorn.conf.py

# Using run script
python run.py prod
```

## Port & Host Configuration

The application runs on port 8080 and localhost (127.0.0.1) by default. To change:

```bash
# For Flask development server (custom port and host)
python app.py --port 9000 --host 0.0.0.0

# For Gunicorn (custom port)
gunicorn app:app -b 0.0.0.0:9000 -c gunicorn.conf.py

# For external access, bind to 0.0.0.0
export FLASK_RUN_HOST=0.0.0.0  # For Flask
gunicorn app:app -b 0.0.0.0:8080  # For Gunicorn
```

## Notes

- Always set `DEBUG_MODE=False` in production environments
- Use the run script for consistent behavior across environments
- Gunicorn provides better performance and stability for production use
- Flask development server is ideal for debugging and development
- **macOS Users**: The run script sets `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` to avoid fork() issues
