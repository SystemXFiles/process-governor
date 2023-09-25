import logging
import sys
import threading
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from time import sleep

import psutil
import pystray
from PIL import Image
from psutil._pswindows import Priority, IOPriority
from pystray import MenuItem

from configuration.config import Config
from resource.resource import get_tray_icon
from service.config_service import ConfigService
from service.rules_service import RulesService


def log_setup(config: Config):
    """
    Configure logging based on the provided configuration.

    Args:
        config (Config): The configuration object containing logging settings.
    """
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


def show_tray():
    """
    Display the system tray icon and menu.

    This function creates a system tray icon with a "Quit" menu option to gracefully exit the application.
    """
    def quit_window(_icon, _):
        _icon.stop()

    menu = (
        MenuItem('Quit', quit_window),
    )

    image = Image.open(get_tray_icon())
    icon = pystray.Icon("tray_icon", image, "Process Governor", menu)
    icon.run()


def main_loop(config: Config):
    """
    Main application loop for applying rules at regular intervals.

    Args:
        config (Config): The configuration object containing rule application settings.
    """
    def loop():
        while True:
            RulesService.apply_rules(config)
            sleep(config.ruleApplyIntervalSeconds)

    thread = threading.Thread(target=loop, name="mainloop")
    thread.daemon = True
    thread.start()


def start_app():
    """
    Start the Process Governor application.

    This function loads the configuration, sets up logging and process priorities, and starts the main application loop.
    """
    try:
        config = ConfigService.load_config()
    except BaseException as e:
        log_setup(Config())
        raise e

    log_setup(config)
    priority_setup()

    main_loop(config)
    show_tray()
