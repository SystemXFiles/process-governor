import logging
import os
from logging import Logger
from typing import Final

import winshell

from constants.app_info import APP_NAME

LOG: Final[Logger] = logging.getLogger('proc-gov')
LOCK_FILE: Final[str] = "pg.lock"

STARTUP_LINK_PATH: Final[str] = os.path.join(winshell.startup(), f"{APP_NAME}.lnk")
STARTUP_TASK_NAME: Final[str] = f"{APP_NAME} Autostart"

CONFIG_FILE_NAME: Final[str] = 'config.json'
CONFIG_FILE_ENCODING: Final[str] = 'utf-8'
