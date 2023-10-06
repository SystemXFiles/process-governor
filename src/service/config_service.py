import json
from abc import ABC
from os.path import exists

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
