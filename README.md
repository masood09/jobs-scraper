# Jobscraper Python

A Flask-based API service for scraping job listings with authorization token support.

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
├── src/
│   └── jobscraper/
│       ├── __init__.py          # Package initialization
│       ├── __main__.py          # Main entry point
│       ├── app.py               # Main Flask application
│       ├── auth.py              # Authentication module
│       └── config.py            # Configuration settings
├── scripts/
│   └── run.py                   # Convenience run script
├── config/
│   └── gunicorn.conf.py         # Gunicorn configuration
├── requirements.txt             # Main requirements
├── pyproject.toml               # Python project configuration
├── .flake8                      # Code style configuration
└── README.md                    # This file
```

## Setup

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

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
python scripts/run.py
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

## Development

The project follows proper Python packaging conventions:

- Source code is located in `src/jobscraper/`
- Uses relative imports within the package
- Includes `__init__.py` and `__main__.py` files
- Follows flake8 coding standards
- Uses pyproject.toml for modern Python packaging

## Contributing

1. Follow the coding conventions in `.flake8`
2. Use the proper package structure
3. Test imports work correctly with the new structure
4. Update documentation when making changes
