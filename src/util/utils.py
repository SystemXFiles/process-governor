import sys
from fnmatch import fnmatch
from functools import lru_cache
from types import NoneType
from typing import get_origin, get_args, Union, Annotated


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

    if pattern:
        pattern = pattern.strip()

    return pattern and fnmatch(name, pattern.strip())


def is_portable():
    """
    Check if the script is running in a portable environment.
    """
    return getattr(sys, 'frozen', False)


def compare_version(version1, version2):
    """
    Compare two version numbers.

    Parameters:
        version1 (str): The first version number.
        version2 (str): The second version number.

    Returns:
        int: 1 if version1 is greater than version2, -1 if version1 is less than version2, 0 if they are equal.
    """
    version1 = version1.lstrip('v')
    version2 = version2.lstrip('v')

    versions1 = [int(v) for v in version1.split(".")]
    versions2 = [int(v) for v in version2.split(".")]

    for i in range(max(len(versions1), len(versions2))):
        v1 = versions1[i] if i < len(versions1) else 0
        v2 = versions2[i] if i < len(versions2) else 0

        if v1 > v2:
            return 1
        elif v1 < v2:
            return -1

    return 0


def extract_type(annotation):
    origin = get_origin(annotation)

    if origin is None:
        return annotation

    args = get_args(annotation)

    if origin == Union:
        non_none_args = [arg for arg in args if arg != NoneType]
        if len(non_none_args) == 1:
            return extract_type(non_none_args[0])
        else:
            return [extract_type(arg) for arg in non_none_args]

    elif origin == Annotated:
        return extract_type(args[0])

    elif args:
        return origin[tuple(extract_type(arg) for arg in args)]

    return annotation


def is_optional_type(annotation):
    if get_origin(annotation) == Union:
        union_args = get_args(annotation)
        for arg in union_args:
            if arg == NoneType or is_optional_type(arg):
                return True
    return False
