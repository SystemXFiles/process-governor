from logging import getLevelName
from typing import Literal

from pydantic import BaseModel, Field


class Logs(BaseModel):
    """
    The Logs class represents the logging configuration for application.

    It defines the settings for enabling/disabling logging, specifying the log file name, log level, maximum log file size,
    and the number of backup log files to keep.
    """

    enable: bool = Field(default=True)
    """
    A boolean flag to enable or disable logging. Default is True (logging is enabled).
    """

    filename: str = Field(default='logging.txt')
    """
    The name of the log file where log messages will be written. Default is 'logging.txt'.
    """

    level: Literal['CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG', 'NOTSET'] = Field(default='INFO')
    """
    The log level for filtering log messages. Default is 'WARN'.
    Valid log levels include: 'CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG', 'NOTSET'.
    """

    maxBytes: int = Field(default=1024 * 1024)
    """
    The maximum size (in bytes) of the log file. When the log file exceeds this size, it will be rotated.
    Default is 1 megabyte (1024 * 1024 bytes).
    """

    backupCount: int = Field(default=2)
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
