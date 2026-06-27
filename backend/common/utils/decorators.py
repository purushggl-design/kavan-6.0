"""
KAVAN v6.0 — Utility Decorators
"""

import functools
import logging
import time
from typing import Callable

logger = logging.getLogger("kavan")


def log_execution_time(func: Callable = None, *, threshold_ms: float = 0):
    """
    Decorator that logs function execution time.

    Args:
        threshold_ms: Only log if execution time exceeds this (ms). 0 = always log.

    Usage:
        @log_execution_time
        def my_function(): ...

        @log_execution_time(threshold_ms=500)
        def slow_function(): ...
    """
    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            start = time.monotonic()
            try:
                result = fn(*args, **kwargs)
                return result
            finally:
                elapsed_ms = (time.monotonic() - start) * 1000
                if elapsed_ms >= threshold_ms:
                    logger.debug(
                        f"{fn.__qualname__} executed in {elapsed_ms:.2f}ms",
                        extra={"kavan_data": {"function": fn.__qualname__, "elapsed_ms": elapsed_ms}},
                    )
        return wrapper

    if func is not None:
        # Called as @log_execution_time without arguments
        return decorator(func)
    return decorator


def handle_service_exception(func: Callable) -> Callable:
    """
    Decorator that catches unexpected exceptions in service methods
    and converts them to KavanBaseException.

    Prevents raw database errors from leaking to the API layer.
    """
    from config.exceptions.base import KavanBaseException

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KavanBaseException:
            # Re-raise known application exceptions as-is
            raise
        except Exception as exc:
            logger.error(
                f"Unexpected error in {func.__qualname__}: {exc}",
                exc_info=True,
            )
            raise KavanBaseException(
                message="An unexpected error occurred. Please try again.",
                code="INTERNAL_ERROR",
            ) from exc

    return wrapper


def retry(max_attempts: int = 3, delay_seconds: float = 1.0, exceptions=(Exception,)):
    """
    Decorator to retry a function on specified exceptions.

    Args:
        max_attempts:  Maximum number of retry attempts
        delay_seconds: Seconds to wait between retries
        exceptions:    Exception types to catch and retry on
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    logger.warning(
                        f"{func.__qualname__} attempt {attempt}/{max_attempts} failed: {exc}"
                    )
                    if attempt < max_attempts:
                        time.sleep(delay_seconds)
            raise last_exc
        return wrapper
    return decorator


def require_permission(permission: str):
    """
    Placeholder decorator for permission checking (Layer 4 — RBAC).
    In Layer 1, this is a no-op that logs the permission check.

    Will be fully implemented in Layer 4.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Layer 4: Check RBAC permission here
            logger.debug(f"Permission check: {permission} (Layer 4 placeholder)")
            return func(*args, **kwargs)
        return wrapper
    return decorator
