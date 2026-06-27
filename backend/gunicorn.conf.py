"""
KAVAN v6.0 — Gunicorn Configuration
============================================================
Production-grade Gunicorn settings.

Reference:
  https://docs.gunicorn.org/en/stable/settings.html
"""

import multiprocessing
import os

# ----------------------------------------------------------
# Server Socket
# ----------------------------------------------------------
bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:8000")
backlog = 2048

# ----------------------------------------------------------
# Workers
# ----------------------------------------------------------
# Formula: (2 * CPU cores) + 1
workers = int(os.environ.get("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "gthread"
threads = int(os.environ.get("GUNICORN_THREADS", 4))
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50  # Randomize restarts to avoid thundering herd

# ----------------------------------------------------------
# Timeouts
# ----------------------------------------------------------
timeout = int(os.environ.get("GUNICORN_TIMEOUT", 30))
graceful_timeout = 30
keepalive = 5

# ----------------------------------------------------------
# Logging
# ----------------------------------------------------------
accesslog = os.environ.get("GUNICORN_ACCESS_LOG", "-")   # stdout
errorlog = os.environ.get("GUNICORN_ERROR_LOG", "-")     # stderr
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")
access_log_format = (
    '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)sμs'
)
capture_output = True
enable_stdio_inheritance = True

# ----------------------------------------------------------
# Process Naming
# ----------------------------------------------------------
proc_name = "kavan-api"

# ----------------------------------------------------------
# Security
# ----------------------------------------------------------
limit_request_line = 8190
limit_request_fields = 100
limit_request_field_size = 8190

# ----------------------------------------------------------
# Server Hooks
# ----------------------------------------------------------

def on_starting(server):
    """Called just before the master process is initialized."""
    server.log.info("KAVAN v6.0 API server starting...")


def when_ready(server):
    """Called just after the server is started."""
    server.log.info(
        f"KAVAN v6.0 API ready on {bind} with {workers} workers"
    )


def worker_init(arbiter, worker):
    """Called just after a worker has been initialized."""
    pass


def worker_exit(arbiter, worker):
    """Called just after a worker has exited."""
    arbiter.log.info(f"Worker {worker.pid} exited.")


def on_exit(server):
    """Called just before exiting."""
    server.log.info("KAVAN v6.0 API server shutting down.")
