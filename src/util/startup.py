import os
import sys

from constants.any import STARTUP_LINK_PATH, STARTUP_TASK_NAME
from constants.resources import STARTUP_SCRIPT
from util.scheduler import TaskScheduler
from util.utils import is_portable


def is_in_startup():
    """
    Check if the current application is set to run during system startup.

    Returns:
        bool: True if the application is set to run during system startup, False otherwise.
    """
    return TaskScheduler.check_task(STARTUP_TASK_NAME)


def add_to_startup():
    """
    Add the current application to the system's startup programs.
    """
    if is_in_startup():
        return

    TaskScheduler.create_startup_task(
        STARTUP_TASK_NAME,
        f"'{STARTUP_SCRIPT}' '{sys.executable}'"
    )


def remove_from_startup():
    """
    Remove the current application from the system's startup programs.
    """
    if is_in_startup():
        TaskScheduler.delete_task(STARTUP_TASK_NAME)


def toggle_startup():
    """
    Toggle the startup status of the application.
    """
    if is_in_startup():
        remove_from_startup()
    else:
        add_to_startup()


def fix_startup():
    """
    Fixes autostart if the app has been moved.
    """
    if not is_portable():
        return

    if not is_in_startup():
        return

    remove_from_startup()
    add_to_startup()
