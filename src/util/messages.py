from enum import IntEnum

from win32api import MessageBoxEx
from win32con import MB_ICONWARNING, MB_ICONINFORMATION, MB_ICONERROR, MB_ICONQUESTION, MB_OK, MB_OKCANCEL, \
    MB_ABORTRETRYIGNORE, MB_YESNOCANCEL, MB_YESNO, MB_RETRYCANCEL, IDOK, IDCANCEL, IDABORT, IDRETRY, IDIGNORE, IDYES, \
    IDNO, IDCLOSE, IDHELP


class MBIcon(IntEnum):
    WARNING = MB_ICONWARNING
    INFORMATION = MB_ICONINFORMATION
    ERROR = MB_ICONERROR
    QUESTION = MB_ICONQUESTION


class MBButton(IntEnum):
    OK = MB_OK
    OKCANCEL = MB_OKCANCEL
    ABORTRETRYIGNORE = MB_ABORTRETRYIGNORE
    YESNOCANCEL = MB_YESNOCANCEL
    YESNO = MB_YESNO
    RETRYCANCEL = MB_RETRYCANCEL


class MBResult(IntEnum):
    OK = IDOK
    CANCEL = IDCANCEL
    ABORT = IDABORT
    RETRY = IDRETRY
    IGNORE = IDIGNORE
    YES = IDYES
    NO = IDNO
    CLOSE = IDCLOSE
    HELP = IDHELP


def message_box(title: str, message: str, icon: MBIcon, btn: MBButton) -> MBResult:
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


def yesno_error_box(title: str, message: str) -> bool:
    """
    Display a yes/no error message box with a specified title and message.

    Args:
        title (str): The title of the message box.
        message (str): The message to be displayed in the message box.

    Returns:
        bool: True if the user clicks "Yes," False if the user clicks "No."
    """
    return message_box(title, message, MBIcon.ERROR, MBButton.YESNO) == MBResult.YES


def show_error(title, message):
    """
    Show an error message box with the given title and message.

    Parameters:
        title (str): The title of the error message box.
        message (str): The message to display in the error message box.
    """
    message_box(title, message, MBIcon.ERROR, MBButton.OK)


def show_info(title, message):
    """
    Show an info message box with the given title and message.

    Parameters:
        title (str): The title of the error message box.
        message (str): The message to display in the error message box.
    """
    message_box(title, message, MBIcon.INFORMATION, MBButton.OK)

