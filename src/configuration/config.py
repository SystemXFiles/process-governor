from dataclasses import dataclass, field
from typing import List

from configuration.logs import Logs
from configuration.rule import Rule


@dataclass
class Config:
    """
    The Config class represents a configuration object for Process Governor.

    It defines the structure of the configuration, including rule application interval, logging settings, and rules.
    """

    ruleApplyIntervalSeconds: int = 1
    """
    The time interval (in seconds) at which rules are applied to processes and services.
    Default is 1 second.
    """

    logging: Logs = field(default_factory=Logs)
    """
    An instance of the Logs class that defines logging settings for Process Governor.
    Default settings are provided by the Logs class.
    """

    rules: List[Rule] = field(default_factory=list)
    """
    A list of Rule objects that specify how Process Governor manages processes and services based on user-defined rules.
    """
