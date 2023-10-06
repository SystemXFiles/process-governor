import logging
import os
import sys
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from threading import Thread
from time import sleep

import psutil
import pystray
from PIL import Image
from psutil._pswindows import Priority, IOPriority
from pystray import MenuItem
from pystray._win32 import Icon

from configuration.config import Config
from resource.resource import get_tray_icon
from service.config_service import ConfigService, CONFIG_FILE_NAME
from service.rules_service import RulesService
from util.utils import yesno_error_box


def log_setup():
    """
    Sets up the logging configuration.

    Retrieves the logging configuration from the `ConfigService` and sets up the logging handlers and formatters
    accordingly. If the logging configuration is disabled, the function does nothing.
    """

    config: Config = ConfigService.load_config()

    if not config.logging.enable:
        return

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    level = config.logging.level_as_int()

    handler = RotatingFileHandler(
        config.logging.filename,
        maxBytes=config.logging.maxBytes,
        backupCount=config.logging.backupCount,
        encoding='utf-8',
    )
    handler.setLevel(level)
    handler.setFormatter(formatter)

    stream_handler = StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(stream_handler)


def priority_setup():
    """
    Set process priority and I/O priority.

    This function sets the process priority to BELOW_NORMAL_PRIORITY_CLASS and the I/O priority to IOPRIO_LOW.
    """
    try:
        process = psutil.Process()
        process.nice(Priority.BELOW_NORMAL_PRIORITY_CLASS)
        process.ionice(IOPriority.IOPRIO_LOW)
    except psutil.Error:
        pass


def init_tray() -> Icon:
    """
    Initializes and returns a system tray icon.

    Returns:
        Icon: The system tray icon.
    """

    config: Config = ConfigService.load_config()
    menu: tuple[MenuItem, ...] = (
        MenuItem('Open JSON config', lambda ico: os.startfile(CONFIG_FILE_NAME)),
        MenuItem('Open log file', lambda ico: os.startfile(config.logging.filename)),
        MenuItem('Quit', lambda ico: ico.stop()),
    )

    image: Image = Image.open(get_tray_icon())
    icon: Icon = pystray.Icon("tray_icon", image, "Process Governor", menu)

    return icon


def main_loop(tray: Icon):
    """
    Main application loop for applying rules at regular intervals, updating the configuration, and managing the system tray icon.

    Args:
        tray (Icon): The system tray icon instance to be managed within the loop. It will be stopped gracefully
            when the loop exits.
    """

    config: Config = ConfigService.load_config()

    try:
        thread = Thread(target=tray.run)
        thread.start()

        while thread.is_alive():
            RulesService.apply_rules(config)
            config = ConfigService.load_config()
            sleep(config.ruleApplyIntervalSeconds)
    except KeyboardInterrupt:
        pass
    except BaseException as e:
        logging.exception(e)

        message = (
            f"An error has occurred in the Process Governor application. To troubleshoot, please check the log "
            f"file: {config.logging.filename} for details.\n\nWould you like to open the log file?"
        )
        title = "Process Governor - Error Detected"

        if yesno_error_box(title, message):
            os.startfile(config.logging.filename)

        raise e
    finally:
        tray.stop()


def start_app():
    """
    Start the Process Governor application.

    This function loads the configuration, sets up logging and process priorities, and starts the main application loop.
    """
    log_setup()
    priority_setup()

    tray: Icon = init_tray()
    main_loop(tray)
