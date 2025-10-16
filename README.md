# Jobscraper Python

A Flask-based API service for scraping job listings with authorization token support.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements/requirements.dev.txt
   ```

2. **Generate API token:**
   ```bash
   export API_ACCESS_TOKEN=$(openssl rand -base64 64)
   ```

3. **Run the service:**
   ```bash
   python -m src.jobscraper
   # or using the run script
   python scripts/run.py dev
   ```

4. **Test the API:**
   ```bash
   curl http://127.0.0.1:8080/health
   ```

## Features

- RESTful API endpoints
- Authorization token authentication
- Job scraping functionality using python-jobspy
- Health check endpoint
- Environment-based configuration
- All scraping parameters are optional with no defaults
- Proper Python package structure

## Project Structure

```
jobscraper-python/
├── src/                         # Source code directory
│   └── jobscraper/              # Main package
│       ├── __init__.py          # Package initialization
│       ├── __main__.py          # Main entry point
│       ├── app.py               # Main Flask application
│       ├── auth.py              # Authentication module
│       └── config.py            # Configuration settings
├── scripts/                     # Utility scripts
│   └── run.py                   # Convenience run script
├── config/                      # Configuration files
│   └── gunicorn.conf.py         # Gunicorn configuration
├── docs/                        # Documentation
│   ├── CODING_CONVENTIONS.md    # Coding standards
│   └── RUNNING.md               # Running instructions
├── tests/                       # Test files
│   ├── __init__.py
│   ├── conftest.py              # Test configuration
│   ├── test_app.py              # Application tests
│   ├── test_auth.py             # Authentication tests
│   ├── test_config.py           # Configuration tests
│   └── test_jobspy.py           # Jobspy integration tests
├── requirements/                # Dependency management
│   ├── requirements.base.txt    # Core dependencies
│   ├── requirements.dev.txt     # Development dependencies
│   ├── requirements.prod.txt    # Production dependencies
│   └── requirements.test.txt    # Test dependencies
├── requirements.txt             # Legacy requirements (points to base.txt)
├── pyproject.toml               # Python project configuration
├── .flake8                      # Code style configuration
├── setup.py                     # Package setup script
└── README.md                    # This file
```

## Setup

1. Install the dependencies:

   **For development (recommended):**
   ```bash
   pip install -r requirements/requirements.dev.txt
   ```
   *Includes core application dependencies plus development tools (testing, linting, formatting)*

   **For production:**
   ```bash
   pip install -r requirements/requirements.prod.txt
   ```
   *Includes core application dependencies plus production server (gunicorn)*

   **Core dependencies only:**
   ```bash
   pip install -r requirements/requirements.base.txt
   ```
   *Only the essential application dependencies without dev/prod extras*

   **Legacy compatibility:**
   ```bash
   pip install -r requirements.txt
   ```
   *Points to base.txt for backward compatibility*

## Modular Requirements Structure

The project uses a modular approach to dependencies management:

### Benefits of Modular Requirements:

- **Separation of Concerns**: Different environments have different dependency needs
- **Reduced Bloat**: Production environments don't install development tools
- **Security**: Production has fewer packages, reducing attack surface
- **Version Control**: Clear separation between core, development, and production dependencies
- **Dependency Tree**: Easy to understand what each environment requires

### Requirements Files Breakdown:

- **requirements/requirements.base.txt**: Core application dependencies (Flask, python-jobspy, etc.)
- **requirements/requirements.dev.txt**: Includes base.txt + development tools (pytest, flake8, black)
- **requirements/requirements.prod.txt**: Includes base.txt + production server (gunicorn)
- **requirements/requirements.test.txt**: Testing-specific dependencies (pytest, pytest-cov)
- **requirements.txt**: Legacy file that references base.txt for compatibility

This structure allows for:
- Cleaner container images (use requirements/requirements.prod.txt for Docker)
- Faster CI/CD pipelines (dev dependencies only in test environments)
- Easier dependency management and updates

2. Generate a secure API access token and set it as an environment variable:
   
   **Generate a secure token:**
   ```bash
   openssl rand -base64 64
   ```
   
   **Set the environment variable:**
   ```bash
   export API_ACCESS_TOKEN="your-generated-secure-token-here"
   ```

## Running the Service

### Development Mode (Using Flask development server)
```bash
# Run directly from the package
python -m src.jobscraper --port 8080 --host 127.0.0.1

# Or using the convenience script
python scripts/run.py dev
```

### Production Mode (Using Gunicorn)
```bash
# Run with Gunicorn
gunicorn src.jobscraper.app:app -b 0.0.0.0:8080 -w 4 -k gthread

# Or with custom configuration
gunicorn src.jobscraper.app:app -c config/gunicorn.conf.py
```

### Custom Port/Host
```bash
# Development on custom port
python -m src.jobscraper --port 9000 --host 0.0.0.0

# Production on custom port
gunicorn src.jobscraper.app:app -b 0.0.0.0:9000 -w 4
```

## API Endpoints

### Public Endpoints (No authentication required)

- `GET /health` - Health check endpoint

### Protected Endpoints (Require authentication)

- `POST /scrape` - Scrape job listings with customizable parameters

## Authentication

All protected endpoints require a valid access token in the Authorization header:

```
Authorization: Bearer your-secret-token-here
```

## /scrape Endpoint

Scrape job listings using the python-jobspy package. All parameters are optional.

**Method:** POST
**Content-Type:** application/json
**Authentication:** Required

### Available Parameters

All parameters from the python-jobspy library are supported:

- `site_name` (list|str): linkedin, zip_recruiter, indeed, glassdoor, google, bayt, bdjobs
- `search_term` (str): Search term for job boards
- `google_search_term` (str): Search term specifically for Google jobs
- `location` (str): Location for job search
- `results_wanted` (int): Number of job results to retrieve
- `hours_old` (int): Filter jobs by hours since posting
- `country_indeed` (str): Country filter for Indeed & Glassdoor
- `distance` (int): Distance in miles (default scope)
- `job_type` (str): fulltime, parttime, internship, contract
- `proxies` (list): Proxy servers in format ['user:pass@host:port', 'localhost']
- `is_remote` (bool): Filter for remote jobs
- `easy_apply` (bool): Filter for easy apply jobs
- `user_agent` (str): Custom user agent string
- `description_format` (str): markdown, html
- `offset` (int): Search result offset
- `verbose` (int): Log verbosity (0-2)
- `linkedin_fetch_description` (bool): Fetch full LinkedIn descriptions
- `linkedin_company_ids` (list[int]): Filter by LinkedIn company IDs
- `enforce_annual_salary` (bool): Convert wages to annual salary
- `ca_cert` (str): Path to CA Certificate file for proxies

### Example Requests

**Basic request:**
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-secret-token-here" \
  -d '{"search_term": "software engineer"}' \
  http://127.0.0.1:8080/scrape
```

**Comprehensive request:**
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-secret-token-here" \
  -d '{
    "site_name": ["indeed", "linkedin"],
    "search_term": "software engineer",
    "location": "San Francisco, CA",
    "results_wanted": 10,
    "hours_old": 72,
    "country_indeed": "USA",
    "is_remote": true,
    "job_type": "fulltime"
  }' \
  http://127.0.0.1:8080/scrape
```

**Health check:**
```bash
curl http://127.0.0.1:8080/health
```

## Expected Responses

### Success (200 OK)
```json
{
  "success": true,
  "count": 15,
  "jobs": [
    {
      "title": "Software Engineer",
      "company": "Tech Company",
      "location": "San Francisco, CA",
      "job_url": "https://example.com/job/123",
      "date_posted": "2023-10-06",
      "is_remote": true
    }
  ]
}
```

### Missing Authorization Header (401 Unauthorized)
```json
{
  "error": "Authorization header required",
  "message": "Please provide an access token in the Authorization header"
}
```

### Invalid Token Format (401 Unauthorized)
```json
{
  "error": "Invalid authorization format",
  "message": "Authorization header should be in format: Bearer <token>"
}
```

### Invalid Access Token (403 Forbidden)
```json
{
  "error": "Invalid access token",
  "message": "The provided access token is not valid"
}
```

### Server Configuration Error (500 Internal Server Error)
```json
{
  "error": "Server configuration error",
  "message": "API access token is not configured"
}
```

### Scraping Error (500 Internal Server Error)
```json
{
  "success": false,
  "error": "Error message details",
  "message": "Failed to scrape jobs"
}
```

## Configuration

The API access token is configured through the `API_ACCESS_TOKEN` environment variable.

### Environment Variables:
- `API_ACCESS_TOKEN` - Required: Your secure API access token
- `DEBUG_MODE` - Optional: True for development, False for production (default: False)
- `LOG_LEVEL` - Optional: DEBUG, INFO, WARNING, ERROR (default: INFO)
- `LOG_TO_FILE` - Optional: True/False to enable file logging (default: False)
- `LOG_FILE_PATH` - Optional: Path to log file (default: app.log)

## Testing

The project includes comprehensive test coverage using pytest.

### Running Tests

**Run all tests:**
```bash
pytest
```

**Run tests with coverage report:**
```bash
pytest --cov=src.jobscraper
```

**Run specific test files:**
```bash
pytest tests/test_app.py
pytest tests/test_auth.py
pytest tests/test_config.py
```

**Run tests with verbose output:**
```bash
pytest -v
```

### Test Structure

Tests are located in the `tests/` directory and include:
- `test_app.py` - Application endpoint tests
- `test_auth.py` - Authentication middleware tests
- `test_config.py` - Configuration validation tests
- `test_jobspy.py` - Jobspy integration tests
- `conftest.py` - Test fixtures and configuration

## Deployment

### Production Deployment

For production deployment, use Gunicorn with the production configuration:

```bash
# Install production dependencies
pip install -r requirements/prod.txt

# Set your API access token
export API_ACCESS_TOKEN="your-secure-token-here"

# Run with Gunicorn using the configuration file
gunicorn src.jobscraper.app:app -c config/gunicorn.conf.py

# Or run with explicit settings
gunicorn src.jobscraper.app:app \
  --bind 0.0.0.0:8080 \
  --workers 4 \
  --worker-class gthread \
  --threads 2 \
  --timeout 30 \
  --access-logfile - \
  --error-logfile -
```

### Environment Configuration

Set the following environment variables for production:

```bash
export API_ACCESS_TOKEN="your-generated-secure-token"
export DEBUG_MODE=False
export LOG_LEVEL=INFO
export LOG_TO_FILE=False
```

### Process Management

For production environments, consider using a process manager like:
- **systemd** for Linux systems
- **supervisord** for process management
- **Docker** for containerized deployment

## Development

The project follows proper Python packaging conventions:

- Source code is located in `src/jobscraper/`
- Uses relative imports within the package
- Includes `__init__.py` and `__main__.py` files
- Follows flake8 coding standards
- Uses pyproject.toml for modern Python packaging
- Includes comprehensive test suite

## Contributing

1. Follow the coding conventions in `.flake8`
2. Use the proper package structure
3. Test imports work correctly with the new structure
4. Write tests for new features and bug fixes
5. Ensure all tests pass before submitting changes
6. Update documentation when making changes
7. Follow the test-driven development approach
