# ============================================================
# KAVAN v6.0 — Advanced Logging Handlers
# ============================================================

import os
from logging.handlers import RotatingFileHandler

class RotatingJSONFileHandler(RotatingFileHandler):
    """
    Custom RotatingFileHandler that ensures the log directory exists
    before attempting to write to the file.
    """
    def __init__(self, filename, mode="a", maxBytes=0, backupCount=0, encoding=None, delay=False, errors=None):
        # Resolve absolute path and ensure the logs directory exists
        log_dir = os.path.dirname(os.path.abspath(filename))
        os.makedirs(log_dir, exist_ok=True)
        
        super().__init__(
            filename=filename,
            mode=mode,
            maxBytes=maxBytes,
            backupCount=backupCount,
            encoding=encoding,
            delay=delay,
            errors=errors
        )
