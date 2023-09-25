from dataclasses import dataclass
from logging import getLevelName
from typing import Literal


@dataclass
class Logs:
    """
    The Logs class represents the logging configuration for Process Governor.

    It defines the settings for enabling/disabling logging, specifying the log file name, log level, maximum log file size,
    and the number of backup log files to keep.
    """

    enable: bool = False
    """
    A boolean flag to enable or disable logging. Default is False (logging is disabled).
    """

    filename: str = 'logging.txt'
    """
    The name of the log file where log messages will be written. Default is 'logging.txt'.
    """

    level: Literal['CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG', 'NOTSET'] = 'WARN'
    """
    The log level for filtering log messages. Default is 'WARN'.
    Valid log levels include: 'CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG', 'NOTSET'.
    """

    maxBytes: int = 1024 * 1024
    """
    The maximum size (in bytes) of the log file. When the log file exceeds this size, it will be rotated.
    Default is 1 megabyte (1024 * 1024 bytes).
    """

    backupCount: int = 2
    """
    The number of backup log files to keep. When log rotation occurs, old log files beyond this count will be deleted.
    Default is 2 backup log files.
    """

    def level_as_int(self):
        """
        Get the log level as an integer value.

        This method converts the log level string into its corresponding integer representation.
        """
        return getLevelName(self.level)
