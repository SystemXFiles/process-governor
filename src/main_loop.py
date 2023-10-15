import os
import traceback
from threading import Thread
from time import sleep
from typing import Optional

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
from util.logs import log_setup, log
from util.messages import message_box, yesno_error_box, MBIcon, show_error


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
    thread = Thread(target=tray.run)
    thread.start()

    log.info('Application started')

    while thread.is_alive():
        RulesService.apply_rules(config)
        config = ConfigService.load_config()
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
