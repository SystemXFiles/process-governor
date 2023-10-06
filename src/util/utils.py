import logging
from contextlib import suppress
from fnmatch import fnmatch
from functools import wraps, lru_cache
from time import time
from typing import Type, TypeVar, Callable, List, Optional

import win32con
from psutil import cpu_times
from win32api import MessageBoxEx

T = TypeVar('T')


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


@lru_cache
def parse_affinity(in_affinity: Optional[str]) -> Optional[List[int]]:
    """
    Parse a CPU core affinity string and return a list of core numbers.

    Args:
        in_affinity (Optional[str]): The CPU core affinity string to parse.

    Returns:
        Optional[List[int]]: A list of CPU core numbers specified in the affinity string.
    """
    if in_affinity is None:
        return None

    affinity = in_affinity.strip()

    if not affinity:
        return list(range(len(cpu_times(percpu=True))))

    affinity = affinity.split(";")
    cores: List[int] = []

    for el in affinity:
        el = el.split('-')

        if len(el) == 2:
            cores.extend(range(int(el[0]), int(el[1]) + 1))
        elif len(el) == 1:
            cores.append(int(el[0]))
        else:
            raise ValueError(in_affinity)

    return cores


@lru_cache
def fnmatch_cached(name: str, pattern: str) -> bool:
    """
    Check if a name matches a pattern using fnmatch, with caching.

    Args:
        name (str): The name to check.
        pattern (str): The pattern to match against.

    Returns:
        bool: True if the name matches the pattern, False otherwise.
    """
    return pattern and fnmatch(name, pattern)


def yesno_error_box(title: str, message: str) -> bool:
    """
    Display a yes/no error message box with a specified title and message.

    Args:
        title (str): The title of the message box.
        message (str): The message to be displayed in the message box.

    Returns:
        bool: True if the user clicks "Yes," False if the user clicks "No."
    """
    return MessageBoxEx(None, message, title, win32con.MB_ICONERROR | win32con.MB_YESNO) == win32con.IDYES
