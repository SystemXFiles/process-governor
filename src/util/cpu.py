from functools import lru_cache
from typing import Optional, List

from psutil import cpu_count


@lru_cache
def parse_affinity(in_affinity: str) -> List[int]:
    """
    Parse a CPU core affinity string and return a list of core numbers.

    Args:
        in_affinity (str): The CPU core affinity string to parse.

    Returns:
        Optional[List[int]]: A list of CPU core numbers specified in the affinity string.
    """
    if in_affinity is None:
        raise ValueError("empty value")

    affinity = in_affinity.strip()

    if not affinity:
        raise ValueError("empty string")

    affinity = affinity.split(";")
    cores: List[int] = []

    try:
        for el in affinity:
            el = list(map(str.strip, el.split('-')))

            if len(el) == 2:
                cores.extend(range(int(el[0]), int(el[1]) + 1))
            elif len(el) == 1:
                cores.append(int(el[0]))
            else:
                raise ValueError("incorrect format")
    except Exception:
        raise ValueError("invalid format. Use range `1-4`, specific cores `0;2;4`, or combination `1;3-5`")

    _check_max_cpu_index(cores)
    return cores


def format_affinity(cores: List[int]) -> Optional[str]:
    """
        Format a list of CPU core numbers into an affinity string.

        Args:
            cores (List[int]): A list of CPU core numbers.

        Returns:
            Optional[str]: An affinity string.
        """
    if cores is None or not cores:
        return None

    # Sort and remove duplicates
    sorted_cores = sorted(set(cores))

    # Group consecutive numbers
    groups = []
    group = [sorted_cores[0]]

    for core in sorted_cores[1:]:
        if core == group[-1] + 1:
            group.append(core)
        else:
            groups.append(group)
            group = [core]
    groups.append(group)

    # Format groups into string
    affinity_str = []

    for group in groups:
        if len(group) == 1:
            affinity_str.append(str(group[0]))
        else:
            affinity_str.append(f"{group[0]}-{group[-1]}")

    result = ";".join(affinity_str)

    _check_max_cpu_index(cores)
    return result


def _check_max_cpu_index(cores):
    available_cores = cpu_count()

    if max(cores) >= available_cores:
        raise ValueError(
            "core count exceeds available CPU cores. "
            f"Maximum available core index is {available_cores - 1}"
        )


if __name__ == '__main__':
    input = "1 ; 3- 5"
    lst = parse_affinity("1;3-5")
    fmt = format_affinity(lst)

    print(input, lst, fmt)

    example_inputs = [[], [0], [1, 2, 3], [0, 2, 4], [1, 3, 4, 5], None]
    for example_cores in example_inputs:
        try:
            print(format_affinity(example_cores))
        except Exception as e:
            print(e)
