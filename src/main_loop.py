import os
import sys
import traceback
from threading import Thread
from time import sleep
from typing import Optional

import psutil
import pystray
from PIL import Image
from psutil._pswindows import Priority, IOPriority
from pystray import MenuItem, Menu
from pystray._win32 import Icon

from configuration.config import Config
from service.config_service import ConfigService, CONFIG_FILE_NAME
from service.rules_service import RulesService
from util.logs import log_setup, log
from util.messages import yesno_error_box, show_error
from util.path import get_tray_icon
from util.startup import is_startup, toggle_startup


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
    image: Image = Image.open(get_tray_icon())
    config: Config = ConfigService.load_config()

    menu: tuple[MenuItem, ...] = (
        MenuItem('Open JSON config', lambda item: os.startfile(CONFIG_FILE_NAME), default=True),

        Menu.SEPARATOR,

        MenuItem('Run on Startup', lambda item: toggle_startup(), lambda item: is_startup(), visible=getattr(sys, 'frozen', False)),
        MenuItem('Open log file', lambda item: os.startfile(config.logging.filename)),

        Menu.SEPARATOR,

        MenuItem('Quit', lambda item: item.stop()),
    )

    return pystray.Icon("tray_icon", image, "Process Governor", menu)


def main_loop(tray: Icon):
    """
    Main application loop for applying rules at regular intervals, updating the configuration, and managing the system tray icon.

    Args:
        tray (Icon): The system tray icon instance to be managed within the loop. It will be stopped gracefully
            when the loop exits.
    """
    thread = Thread(target=tray.run)
    thread.start()

    log.info('Application started')

    config: Optional[Config] = None
    is_changed: bool

    while thread.is_alive():
        config, is_changed = ConfigService.reload_if_changed(config)

        RulesService.apply_rules(config, is_changed)
        sleep(config.ruleApplyIntervalSeconds)

    log.info('The application has stopped')


def start_app():
    """
    Start the Process Governor application.

    This function loads the configuration, sets up logging and process priorities, and starts the main application loop.
    """
    tray: Optional[Icon] = None

    try:
        log_setup()
        priority_setup()

        tray: Icon = init_tray()
        main_loop(tray)
    except KeyboardInterrupt:
        pass
    except BaseException as e:
        log.exception(e)

        config: Optional[Config] = None

        try:
            config = ConfigService.load_config()
        except:
            pass

        title = "Process Governor - Error Detected"

        if config:
            message = (
                f"An error has occurred in the Process Governor application. To troubleshoot, please check the log "
                f"file: {config.logging.filename} for details.\n\nWould you like to open the log file?"
            )

            if yesno_error_box(title, message):
                os.startfile(config.logging.filename)
        else:
            message = f"An error has occurred in the Process Governor application.\n\n" + traceback.format_exc()
            show_error(title, message)
    finally:
        if tray:
            tray.stop()
