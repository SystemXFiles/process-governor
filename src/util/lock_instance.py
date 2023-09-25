import os
import sys

import psutil


def is_process_running(pid):
    """
    Check if a process with the given PID is running.

    Args:
        pid: The process ID (PID) to check.

    Returns:
        bool: True if the process is running, False otherwise.
    """
    try:
        process = psutil.Process(pid)
        return process.is_running()
    except psutil.NoSuchProcess:
        return False


def create_lock_file():
    """
    Create a lock file to prevent multiple instances of a process from running simultaneously.

    If the lock file already exists, it checks if the process that created it is still running. If it is,
    the current process exits to avoid running multiple instances.

    If the lock file does not exist or the process is no longer running, it creates the lock file with the
    current process's PID.
    """
    lock_file = "pg.lock"

    if os.path.isfile(lock_file):
        # Check if the process that created the lock file is still running
        with open(lock_file, "r") as file:
            pid = int(file.read().strip())

            if is_process_running(pid):
                sys.exit(1)

    # Create the lock file with the current process's PID
    with open(lock_file, "w") as file:
        file.write(str(os.getpid()))
