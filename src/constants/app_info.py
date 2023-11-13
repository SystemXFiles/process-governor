import os
import sys
from typing import Final

from util.utils import is_portable

APP_NAME: Final[str] = "Process Governor"
APP_VERSION: Final[str] = "1.1.4"
APP_AUTHOR: Final[str] = "System X - Files"

CURRENT_TAG: Final[str] = f"v{APP_VERSION}"
APP_NAME_WITH_VERSION: Final[str] = f"{APP_NAME} {CURRENT_TAG}"

if is_portable():
    APP_PATH: Final[str] = sys._MEIPASS
else:
    APP_PATH: Final[str] = os.getcwd()
