import os
import sys
from typing import Final

from util.utils import is_portable

APP_AUTHOR: Final[str] = "System X - Files"
APP_NAME: Final[str] = "Process Governor"
APP_VERSION: Final[str] = "1.3.1"
APP_PROCESSES = {f"{APP_NAME}.exe", "python.exe"}

CURRENT_TAG: Final[str] = f"v{APP_VERSION}"
APP_NAME_WITH_VERSION: Final[str] = f"{APP_NAME} {CURRENT_TAG}"
APP_TITLE = f"{APP_NAME_WITH_VERSION} by {APP_AUTHOR}"
TITLE_ERROR: Final[str] = f"Error Detected - {APP_NAME_WITH_VERSION}"

if is_portable():
    APP_PATH: Final[str] = sys._MEIPASS
else:
    APP_PATH: Final[str] = os.getcwd()

STARTUP_TASK_NAME: Final[str] = f"{APP_NAME} Autostart"
