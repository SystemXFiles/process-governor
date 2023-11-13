import logging
import os
from typing import Final

import winshell

from constants.app_info import APP_NAME

LOG = logging.getLogger('proc-gov')
CONFIG_FILE_NAME: Final[str] = 'config.json'
LOCK_FILE: Final[str] = "pg.lock"

STARTUP_LINK_PATH: Final[str] = os.path.join(winshell.startup(), f"{APP_NAME}.lnk")
STARTUP_TASK_NAME: Final[str] = f"{APP_NAME} Autostart"
