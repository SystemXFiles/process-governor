import os
import traceback
from threading import Thread
from time import sleep
from typing import Optional

import psutil
from psutil._pswindows import Priority, IOPriority
from pystray._win32 import Icon

from configuration.config import Config
from constants.any import LOG
from constants.app_info import APP_NAME_WITH_VERSION, APP_NAME
from service.config_service import ConfigService
from service.rules_service import RulesService
from ui.tray import init_tray
from util.logs import log_setup
from util.messages import yesno_error_box, show_error
from util.startup import remove_old_startup_method, fix_startup


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


def main_loop(tray: Icon):
    """
    Main application loop for applying rules at regular intervals, updating the configuration, and managing the system tray icon.

    Args:
        tray (Icon): The system tray icon instance to be managed within the loop. It will be stopped gracefully
            when the loop exits.
    """
    thread = Thread(target=tray.run)
    thread.start()

    LOG.info('Application started')

    config: Optional[Config] = None
    is_changed: bool

    while thread.is_alive():
        config, is_changed = ConfigService.reload_if_changed(config)

        RulesService.apply_rules(config, is_changed)
        sleep(config.ruleApplyIntervalSeconds)

    LOG.info('The application has stopped')


def start_app():
    """
    Start application.

    This function loads the configuration, sets up logging and process priorities, and starts the main application loop.
    """
    tray: Optional[Icon] = None

    try:
        fix_startup()
        remove_old_startup_method()
        log_setup()
        priority_setup()

        tray: Icon = init_tray()
        main_loop(tray)
    except KeyboardInterrupt:
        pass
    except BaseException as e:
        LOG.exception(e)

        config: Optional[Config] = None

        try:
            config = ConfigService.load_config()
        except:
            pass

        title = f"{APP_NAME_WITH_VERSION} - Error Detected"

        if config:
            message = (
                f"An error has occurred in the {APP_NAME} application. To troubleshoot, please check the log "
                f"file: {config.logging.filename} for details.\n\nWould you like to open the log file?"
            )

            if yesno_error_box(title, message):
                os.startfile(config.logging.filename)
        else:
            message = f"An error has occurred in the {APP_NAME} application.\n\n" + traceback.format_exc()
            show_error(title, message)
    finally:
        if tray:
            tray.stop()
