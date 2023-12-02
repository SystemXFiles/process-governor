from typing import List

from pydantic import BaseModel, Field

from configuration.logs import Logs
from configuration.rule import Rule


class Config(BaseModel):
    """
    The Config class represents a configuration object for application.

    It defines the structure of the configuration, including rule application interval, logging settings, and rules.
    """

    ruleApplyIntervalSeconds: int = Field(default=1)
    """
    The time interval (in seconds) at which rules are applied to processes and services.
    Default is 1 second.
    """

    logging: Logs = Field(default_factory=Logs)
    """
    An instance of the Logs class that defines logging settings for application.
    Default settings are provided by the Logs class.
    """

    rules: List[Rule] = Field(default_factory=list)
    """
    A list of Rule objects that specify how application manages processes and services based on user-defined rules.
    """
