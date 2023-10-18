import os
import sys

import winshell


def startup_link_path():
    """
    Returns the path to the startup link file for the "Process Governor" application.
    The startup link file is located in the Windows startup folder.

    :return: A string representing the path to the startup link file.
    """
    return os.path.join(winshell.startup(), "Process Governor.lnk")


def is_startup():
    """
    Check if the startup link path exists as a file.
    """
    return os.path.isfile(startup_link_path())


def create_startup_link():
    """
    Create a shortcut in the Windows startup folder.
    """
    link_path = startup_link_path()

    if os.path.isfile(link_path):
        return

    with winshell.shortcut(link_path) as link:
        link.path = f"\"{sys.executable}\""
        link.description = "Process Governor"
        link.icon_location = (sys.executable, 0)
        link.working_directory = os.getcwd()

        if not getattr(sys, 'frozen', False):
            link.arguments = f"\"{sys.argv[0]}\""


def remove_startup_link():
    """
    Remove the startup file.
    """
    link_path = startup_link_path()

    if os.path.isfile(link_path):
        os.remove(link_path)


def toggle_startup():
    """
    Toggle the startup link based on whether it currently exists or not.

    Parameters:
        None

    Returns:
        None
    """
    if is_startup():
        remove_startup_link()
    else:
        create_startup_link()
