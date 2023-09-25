from dataclasses import dataclass
from typing import List, Optional

import psutil
from psutil._pswindows import Priority, IOPriority


@dataclass
class Process:
    """
    The Process class represents information about a running process in Process Governor.

    It includes attributes such as process ID (pid), executable name (exe), process name (name), priority (nice), I/O priority
    (ionice), CPU core affinity, and the associated psutil.Process object.
    """

    pid: int
    """
    The unique identifier of the process (Process ID).
    """

    exe: str
    """
    The name of the executable file associated with the process.
    """

    name: str
    """
    The name of the process.
    """

    nice: Optional[Priority]
    """
    The priority level of the process (nice). Default is None (no priority specified).
    """

    ionice: Optional[IOPriority]
    """
    The I/O priority of the process (ionice). Default is None (no I/O priority specified).
    """

    affinity: List[int]
    """
    A list of integers representing the CPU cores to which the process is bound (CPU core affinity).
    """

    process: psutil.Process
    """
    The psutil.Process object associated with the process, providing access to additional process information and control.
    """
