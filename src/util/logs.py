import logging
import sys
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

from configuration.logs import Logs
from constants.any import LOG, LOG_FILE_NAME
from service.config_service import ConfigService


def log_setup():
    """
    Sets up the logging configuration.

    Retrieves the logging configuration from the `ConfigService` and sets up the logging handlers and formatters
    accordingly. If the logging configuration is disabled, the function does nothing.
    """

    log_cfg: Logs = Logs()
    exception = None

    try:
        log_cfg = ConfigService.load_logs()
    except BaseException as e:
        exception = e
        pass

    LOG.setLevel(log_cfg.level_as_int())

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    LOG.addHandler(console_handler)

    if not log_cfg.enable:
        return

    file_handler = RotatingFileHandler(
        LOG_FILE_NAME,
        maxBytes=log_cfg.maxBytes,
        backupCount=log_cfg.backupCount,
        encoding='utf-8',
    )
    file_handler.setFormatter(formatter)
    LOG.addHandler(file_handler)

    if exception:
        raise exception
