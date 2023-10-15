import logging
import sys
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

from configuration.config import Config
from service.config_service import ConfigService

log = logging.getLogger('proc-gov')


def log_setup():
    """
    Sets up the logging configuration.

    Retrieves the logging configuration from the `ConfigService` and sets up the logging handlers and formatters
    accordingly. If the logging configuration is disabled, the function does nothing.
    """

    config: Config = ConfigService.load_config()

    if not config.logging.enable:
        return

    console_handler = StreamHandler(sys.stdout)
    file_handler = RotatingFileHandler(
        config.logging.filename,
        maxBytes=config.logging.maxBytes,
        backupCount=config.logging.backupCount,
        encoding='utf-8',
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    log.setLevel(config.logging.level_as_int())
    log.addHandler(file_handler)
    log.addHandler(console_handler)
