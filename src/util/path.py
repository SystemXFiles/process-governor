import os
import sys


def get_root():
    """
    Retrieves the root directory of the application.

    Returns:
        str: The absolute path of the root directory.

    Note:
        This function checks if the application is running in a frozen state (e.g.,
        as an executable) and retrieves the root directory accordingly.
        If the application is not frozen, it retrieves the current working directory.

    """
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.getcwd()

    return application_path


def get_tray_icon() -> str:
    """
    Get the path to the tray icon file.

    Returns:
        str: The path to the tray icon file.
    """
    return f"{get_root()}/resources/app.ico"


def get_startup_script() -> str:
    """
    Returns the path to the startup script.

    Returns:
        str: The path to the startup script.
    """
    return f"{get_root()}/resources/startup.bat"

