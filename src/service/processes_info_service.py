from abc import ABC

import psutil
from psutil import NoSuchProcess

from model.process import Process


class ProcessesInfoService(ABC):
    """
    The ProcessesInfoService class provides methods for retrieving information about running processes in Process Governor.
    It is an abstract base class (ABC) to be subclassed by specific implementation classes.
    """

    @staticmethod
    def get_list() -> dict[int, Process]:
        """
        Get a dictionary of running processes and their information.

        Returns:
            dict[int, Process]: A dictionary where keys are process IDs (pids) and values are Process objects
            representing the running processes.
        """
        result: dict[int, Process] = {}

        for process in psutil.process_iter():
            try:
                info = process.as_dict(attrs=['name', 'exe', 'nice', 'ionice', 'cpu_affinity'])
                result[process.pid] = Process(
                    process.pid,
                    info['exe'],
                    info['name'],
                    info['nice'],
                    info['ionice'],
                    info['cpu_affinity'],
                    process
                )
            except NoSuchProcess as _:
                pass

        return result

    __prev_pids: list[int] = []

    @classmethod
    def get_new_processes(cls) -> dict[int, Process]:
        """
        Get a dictionary of newly created processes since the last check.

        Returns:
            dict[int, Process]: A dictionary where keys are process IDs (pids) and values are Process objects
            representing the newly created processes.
        """
        result: dict[int, Process] = {}
        current_pids = psutil.pids()

        for pid in current_pids:
            if pid not in cls.__prev_pids:
                try:
                    process = psutil.Process(pid)
                    info = process.as_dict(attrs=['name', 'exe', 'nice', 'ionice', 'cpu_affinity'])
                    result[pid] = Process(
                        pid,
                        info['exe'],
                        info['name'],
                        int(info['nice']) if info['nice'] else None,
                        int(info['ionice']) if info['ionice'] else None,
                        info['cpu_affinity'],
                        process
                    )
                except NoSuchProcess as _:
                    pass

        cls.__prev_pids = current_pids

        return result
