import os
import webbrowser

import pystray
from PIL import Image
from pystray import MenuItem, Menu
from pystray._win32 import Icon

from constants.any import CONFIG_FILE_NAME, LOG_FILE_NAME
from constants.app_info import APP_NAME_WITH_VERSION, APP_NAME
from constants.resources import APP_ICON
from constants.updates import UPDATE_URL
from ui.editor import open_rule_editor
from util.messages import yesno_error_box, show_error, show_info
from util.startup import toggle_startup, is_in_startup
from util.updates import check_latest_version
from util.utils import is_portable


def check_updates():
    """
    Check for updates and display appropriate messages depending on the result.

    Returns:
        None
    """

    latest_version = check_latest_version()

    if latest_version is None:
        show_error(
            f"Error Detected - {APP_NAME_WITH_VERSION}",
            "Failed to check for updates. Please check your internet connection."
        )
    elif not latest_version:
        show_info(
            APP_NAME_WITH_VERSION,
            "You are using the latest version."
        )
    else:
        message = (
            f"A new version {latest_version} is available. Would you like to update {APP_NAME} now?"
        )

        if yesno_error_box(APP_NAME_WITH_VERSION, message):
            webbrowser.open(UPDATE_URL, new=0, autoraise=True)


def init_tray() -> Icon:
    """
    Initializes and returns a system tray icon.

    Returns:
        Icon: The system tray icon.
    """
    image: Image = Image.open(APP_ICON)

    menu: tuple[MenuItem, ...] = (
        MenuItem(APP_NAME_WITH_VERSION, None, enabled=False),
        Menu.SEPARATOR,

        MenuItem('Configure Rules', lambda item: open_rule_editor(), default=True),
        Menu.SEPARATOR,

        MenuItem('Open config file', lambda item: os.startfile(CONFIG_FILE_NAME)),
        MenuItem('Open log file', lambda item: os.startfile(LOG_FILE_NAME)),
        Menu.SEPARATOR,

        MenuItem(
            'Run on Startup',
            lambda item: toggle_startup(),
            lambda item: is_in_startup(),
            visible=is_portable()
        ),
        MenuItem(
            'Check for Updates',
            lambda item: check_updates()
        ),
        Menu.SEPARATOR,

        MenuItem('Quit', lambda item: item.stop()),
    )

    return pystray.Icon("tray_icon", image, APP_NAME, menu)
