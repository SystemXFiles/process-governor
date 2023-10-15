import platform
import sys

import pyuac

from main_loop import start_app
from util.lock_instance import create_lock_file, remove_lock_file
from util.messages import message_box, MBIcon

if __name__ == "__main__":
    if not platform.system() == "Windows":
        print("Process Governor is intended to run on Windows only.")
        sys.exit(1)

    if not pyuac.isUserAdmin():
        message_box(
            "Process Governor",
            "This program requires administrator privileges to run.\n"
            "Please run the program as an administrator to ensure proper functionality.",
            MBIcon.INFORMATION
        )
        sys.exit(1)

    create_lock_file()
    try:
        start_app()
    finally:
        remove_lock_file()
