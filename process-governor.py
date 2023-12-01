import platform
import sys

import pyuac

from constants.app_info import APP_NAME, APP_NAME_WITH_VERSION
from main_loop import start_app
from util.lock_instance import create_lock_file, remove_lock_file
from util.messages import show_error

if __name__ == "__main__":
    if not platform.system() == "Windows":
        print(f"{APP_NAME} is intended to run on Windows only.")
        sys.exit(1)

    if not pyuac.isUserAdmin():
        show_error(
            f"Error Detected - {APP_NAME_WITH_VERSION}",
            "This program requires administrator privileges to run.\n"
            "Please run the program as an administrator to ensure proper functionality."
        )
        sys.exit(1)

    create_lock_file()
    try:
        start_app()
    finally:
        remove_lock_file()
