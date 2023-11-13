import logging
import sys
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

from configuration.config import Config
from constants.any import LOG
from service.config_service import ConfigService


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

    LOG.setLevel(config.logging.level_as_int())
    LOG.addHandler(file_handler)
    LOG.addHandler(console_handler)
