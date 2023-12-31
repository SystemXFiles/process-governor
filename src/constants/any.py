import logging
from logging import Logger
from typing import Final

from constants.app_info import APP_NAME

LOG: Final[Logger] = logging.getLogger("proc-gov")
LOG_FILE_NAME: Final[str] = "logging.txt"
LOCK_FILE_NAME: Final[str] = "pg.lock"

STARTUP_TASK_NAME: Final[str] = f"{APP_NAME} Autostart"

CONFIG_FILE_NAME: Final[str] = "config.json"
CONFIG_FILE_ENCODING: Final[str] = "utf-8"

BOTH_SELECTORS_SET: Final[str] = "both_selectors_set"
