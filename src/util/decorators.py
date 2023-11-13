import logging
import threading
from contextlib import suppress
from functools import wraps
from time import time
from typing import Callable, Optional, Type, TypeVar

from constants.any import LOG


def run_in_thread(non_reentrant=True):
    """
    Decorator to run a function in a separate thread. Prevents re-entry of the function while it is still running.
    Includes a method to check if the function is currently running.

    Args:
        non_reentrant (bool): If True, prevents re-invocation of the function while it is already running.
    """

    def decorator(func):
        func._is_running = False

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal func
            if non_reentrant and func._is_running:
                LOG.debug(f"Function {func.__name__} is already running.")
                return

            def run():
                nonlocal func
                try:
                    func._is_running = True
                    func(*args, **kwargs)
                finally:
                    func._is_running = False

            thread = threading.Thread(target=run)
            thread.start()

        def is_running():
            """Returns True if the function is currently running."""
            return func._is_running

        wrapper.is_running = is_running
        return wrapper

    return decorator


T = TypeVar('T')


def cached(timeout_in_seconds, logged=False) -> Callable[..., T]:
    """
    Decorator that caches the results of a function for a specified timeout.

    Args:
        timeout_in_seconds (int): The cache timeout duration in seconds.
        logged (bool, optional): Whether to log cache initialization and hits (default is False).

    Returns:
        Callable: A decorated function with caching capabilities.
    """

    def decorator(function: Callable[..., T]) -> Callable[..., T]:
        if logged:
            logging.info("-- Initializing cache for", function.__name__)

        cache = {}

        @wraps(function)
        def decorated_function(*args, **kwargs) -> T:
            if logged:
                logging.info("-- Called function", function.__name__)

            key = args, frozenset(kwargs.items())
            result: Optional[tuple[T]] = None

            if key in cache:
                if logged:
                    logging.info("-- Cache hit for", function.__name__, key)

                cache_hit, expiry = cache[key]

                if time() - expiry < timeout_in_seconds:
                    result = cache_hit
                elif logged:
                    logging.info("-- Cache expired for", function.__name__, key)
            elif logged:
                logging.info("-- Cache miss for", function.__name__, key)

            if result is None:
                result = (function(*args, **kwargs),)
                cache[key] = result, time()

            return result[0]

        return decorated_function

    return decorator


def suppress_exception(function: Callable[..., T], *exception_type: Type[BaseException]) -> Callable[..., T]:
    """
    Decorator that suppresses specified exceptions raised by a function.

    Args:
        function (Callable): The function to decorate.
        *exception_type (Type[BaseException]): Variable number of exception types to suppress.

    Returns:
        Callable: A decorated function that suppresses the specified exceptions.
    """
    if getattr(function, '__suppressed__', False):
        return function

    exception_type = exception_type or [type(BaseException)]

    @wraps(function)
    def wrapper(*args, **kwargs) -> Callable[..., T]:
        with suppress(*exception_type):
            return function(*args, **kwargs)

    wrapper.__suppressed__ = True

    return wrapper
