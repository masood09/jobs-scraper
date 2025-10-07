"""
Gunicorn configuration file for production deployment.
"""

import multiprocessing

# Server socket
bind = "0.0.0.0:8080"  # Can be overridden with -b flag

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 4

# Logging
accesslog = "-"  # stdout
errorlog = "-"  # stdout
loglevel = "info"

# Process naming
proc_name = "jobscraper-api"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Worker processes timeout
timeout = 30
keepalive = 2

# SSL (uncomment and configure if using SSL)
# keyfile = "/path/to/your/keyfile.key"
# certfile = "/path/to/your/certificate.crt"


# Server hooks
def on_starting(server):
    print("JobScraper API server is starting...")


def when_ready(server):
    print("JobScraper API server is ready to accept connections")


def on_exit(server):
    print("JobScraper API server is shutting down...")
