import os
import traceback
from threading import Thread
from time import sleep
from typing import Optional

import psutil
from psutil._pswindows import Priority, IOPriority
from pystray._win32 import Icon

from configuration.config import Config
from configuration.logs import Logs
from constants.any import LOG, LOG_FILE_NAME
from constants.app_info import APP_NAME_WITH_VERSION, APP_NAME
from constants.ui import RC_TITLE
from service.config_service import ConfigService
from service.rules_service import RulesService
from ui.editor import open_rule_editor, is_editor_open
from ui.tray import init_tray
from util.logs import log_setup
from util.messages import yesno_error_box, show_error
from util.startup import fix_startup


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
    last_error_message = None

    while thread.is_alive():
        try:
            config, is_changed = ConfigService.reload_if_changed(config)
            RulesService.apply_rules(config, is_changed)
            last_error_message = None
        except BaseException as e:
            if not config:
                config = Config()

            current_error_message = str(e)

            if current_error_message != last_error_message:
                LOG.exception("Error in the loop of loading and applying rules.")

                last_error_message = current_error_message

                if ConfigService.rules_has_error():
                    show_rules_error_message()
                else:
                    show_abstract_error_message(False)

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
        log_setup()
        priority_setup()

        tray: Icon = init_tray()
        main_loop(tray)
    except KeyboardInterrupt:
        pass
    except:
        LOG.exception("A critical error occurred, causing the application to stop.")
        show_abstract_error_message(True)
    finally:
        if tray:
            tray.stop()


def show_rules_error_message():
    title = f"Error Detected - {APP_NAME_WITH_VERSION}"
    message = "An error has occurred while loading or applying the rules.\n"

    if is_editor_open:
        message += "Please check the correctness of the rules."
        show_error(title, message)
    else:
        message += f"Would you like to open the {RC_TITLE} to review and correct the rules?"
        if yesno_error_box(title, message):
            open_rule_editor()


def show_abstract_error_message(will_closed: bool):
    title = f"Error Detected - {APP_NAME_WITH_VERSION}"
    will_closed_text = 'The application will now close.' if will_closed else ''
    message = (
        f"An error has occurred in the {APP_NAME} application. {will_closed_text}\n"
        f"To troubleshoot, please check the log file `{LOG_FILE_NAME}` for details.\n\n"
        f"Would you like to open the log file?"
    )

    if yesno_error_box(title, message):
        os.startfile(LOG_FILE_NAME)
