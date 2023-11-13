import sys
from fnmatch import fnmatch
from functools import lru_cache
from typing import List, Optional

from psutil import cpu_times


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
