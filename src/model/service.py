from dataclasses import dataclass
from typing import Optional


@dataclass
class Service:
    """
    The Service class represents information about a Windows service.

    It includes attributes such as service process ID (pid), service name, display name, description, current status,
    and binary path.
    """

    pid: int
    """
    The process ID (pid) associated with the Windows service.
    """

    name: str
    """
    The name of the Windows service.
    """

    display_name: str
    """
    The display name of the Windows service.
    """

    description: Optional[str]
    """
    A description of the Windows service. Default is None (no description available).
    """

    status: str
    """
    The current status of the Windows service.
    """

    binpath: str
    """
    The binary path of the Windows service, specifying the location of the service executable.
    """
