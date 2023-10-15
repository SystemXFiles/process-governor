import os
import sys


def get_root():
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
