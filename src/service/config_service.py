from abc import ABC
from os.path import exists

import jsonpickle
from jsonpickle import util

from configuration.config import Config

CONFIG_FILE_NAME = 'config.json'


def items_without_null_fields(obj):
    """
    Generator function that yields key-value pairs from a dictionary, excluding fields with None values.

    Args:
        obj (dict): The dictionary to iterate over.

    Yields:
        tuple: A tuple containing a key and its corresponding non-None value from the dictionary.
    """
    for k, v in obj.items():
        if v is not None:
            yield k, v


class ConfigService(ABC):
    """
    The ConfigService class provides methods for saving and loading configuration settings for Process Governor.
    It is an abstract base class (ABC) to be subclassed by specific implementation classes.
    """

    @classmethod
    def save_config(cls, config: Config):
        """
        Save the provided configuration object to a JSON file.

        Args:
            config (Config): The configuration object to be saved.
        """
        original = util.items
        util.items = items_without_null_fields

        try:
            with open(CONFIG_FILE_NAME, 'w') as file:
                file.write(jsonpickle.encode(config, indent=4, make_refs=False))
        finally:
            util.items = original

    @classmethod
    def load_config(cls) -> Config:
        """
        Load the configuration from a JSON file or create a new one if the file doesn't exist.

        Returns:
            Config: The loaded or newly created configuration object.
        """
        if exists(CONFIG_FILE_NAME):
            with open(CONFIG_FILE_NAME, 'r') as file:
                config = jsonpickle.decode(file.read())
        else:
            cls.save_config(config := Config())

        return config
