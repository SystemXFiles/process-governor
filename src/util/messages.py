import threading

from win32api import MessageBoxEx

from constants.app_info import APP_NAME_WITH_VERSION, TITLE_ERROR, APP_TITLE
from enums.messages import MBIcon, MBButton, MBResult


def _message_box(title: str, message: str, icon: MBIcon, btn: MBButton) -> MBResult:
    """
    Display a message box with the specified title, message, icon, and button.

    Args:
        title (str): The title of the message box.
        message (str): The message to be displayed in the message box.
        icon (MBIcon): The icon to be displayed in the message box.
        btn (MBButton): The button(s) to be displayed in the message box.

    Returns:
        MBResult: The result of the message box operation.
    """
    return MessageBoxEx(None, message, title, icon | btn)


def show_info(message: str, title: str = APP_TITLE):
    threading.Thread(target=lambda: _message_box(title, message, MBIcon.INFORMATION, MBButton.OK)).start()


def yesno_info_box(message: str, title: str = APP_TITLE) -> bool:
    return _message_box(title, message, MBIcon.INFORMATION, MBButton.YESNO) == MBResult.YES


def yesno_question_box(message: str, title: str = APP_TITLE) -> bool:
    return _message_box(title, message, MBIcon.QUESTION, MBButton.YESNO) == MBResult.YES


def show_error(message: str, title: str = TITLE_ERROR):
    threading.Thread(target=lambda: _message_box(title, message, MBIcon.ERROR, MBButton.OK)).start()


def yesno_error_box(message: str, title: str = TITLE_ERROR) -> bool:
    return _message_box(title, message, MBIcon.ERROR, MBButton.YESNO) == MBResult.YES
