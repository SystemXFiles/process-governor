import json
import os.path
from abc import ABC
from os.path import exists
from typing import Optional

from configuration.config import Config
from util.utils import cached

CONFIG_FILE_NAME = 'config.json'


class ConfigService(ABC):
    """
    ConfigService is responsible for managing the application's configuration data.

    This class provides methods for saving, loading, and accessing the configuration.
    """

    @classmethod
    def save_config(cls, config: Config):
        """
        Save the provided configuration object to a JSON file.

        If the configuration is not initialized, it creates a new one.

        Args:
            config (Config): The configuration object to be saved.
        """
        if config is None:
            config = Config()

        with open(CONFIG_FILE_NAME, 'w') as file:
            json = config.model_dump_json(indent=4, exclude_none=True)
            file.write(json)

    @classmethod
    @cached(1)
    def load_config(cls) -> Config:
        """
        Load the configuration from a JSON file or create a new one if the file doesn't exist.

        Returns:
            Config: The loaded or newly created configuration object.
        """
        if not exists(CONFIG_FILE_NAME):
            cls.save_config(config := Config())
            return config

        with open(CONFIG_FILE_NAME, 'r') as file:
            return Config(**json.load(file))

    __prev_mtime = 0

    @classmethod
    def reload_if_changed(cls, prev_config: Optional[Config]) -> tuple[Config, bool]:
        """
        Reloads the configuration if it has changed since the last reload and returns the updated configuration and a flag indicating whether the configuration has changed.

        Parameters:
            prev_config (Optional[Config]): The previous configuration object. Can be None if there is no previous configuration.

        Returns:
            tuple[Config, bool]: A tuple containing the updated configuration object and a boolean flag indicating whether the configuration has changed. If the configuration has changed or there is no previous configuration, the updated configuration is loaded from the file. Otherwise, the previous configuration is returned.
        """
        current_mtime = os.path.getmtime(CONFIG_FILE_NAME)
        is_changed = current_mtime > cls.__prev_mtime

        cls.__prev_mtime = current_mtime

        if is_changed or prev_config is None:
            return cls.load_config(), True

        return prev_config, False
