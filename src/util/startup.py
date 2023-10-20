import os
import sys

import winshell

from util.path import get_startup_script
from util.utils import is_portable

__STARTUP_LINK_PATH = os.path.join(winshell.startup(), "Process Governor.lnk")


def __create_startup_link():
    """
    Creates a startup link for the application.
    """
    with winshell.shortcut(__STARTUP_LINK_PATH) as link:
        link.path = f"\"{get_startup_script()}\""
        link.description = "Process Governor"
        link.icon_location = (sys.executable, 0)
        link.working_directory = os.getcwd()
        link.arguments = f"\"{sys.executable}\""


def is_in_startup():
    """
    Check if the startup link path exists as a file.
    """
    return os.path.isfile(__STARTUP_LINK_PATH)


def add_to_startup():
    """
    Create a shortcut in the Windows startup folder.
    """
    if os.path.isfile(__STARTUP_LINK_PATH):
        return

    __create_startup_link()


def remove_from_startup():
    """
    Remove the startup file.
    """
    if os.path.isfile(__STARTUP_LINK_PATH):
        os.remove(__STARTUP_LINK_PATH)


def toggle_startup():
    """
    Toggle the startup link based on whether it currently exists or not.

    Parameters:
        None

    Returns:
        None
    """
    if is_in_startup():
        remove_from_startup()
    else:
        add_to_startup()


def fix_startup():
    """
    Fix the startup by creating a startup link if the system is portable and the startup link path exists.
    """
    if not is_portable():
        return

    if not os.path.isfile(__STARTUP_LINK_PATH):
        return

    __create_startup_link()
