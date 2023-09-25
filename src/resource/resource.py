import os


def get_tray_icon() -> str:
    """
    Get the path to the tray icon file.

    This function checks if the icon file "favicon.ico" exists in the "resource" directory. If it exists, the
    full path to the icon file is returned. If not found, it returns the path relative to the "src" directory.

    Returns:
        str: The path to the tray icon file.
    """
    icon_name = "resource/favicon.ico"

    if os.path.isfile(icon_name):
        return icon_name

    return f"src/{icon_name}"
