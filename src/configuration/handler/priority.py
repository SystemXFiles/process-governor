from psutil._pswindows import Priority
from pydantic import PlainSerializer, WithJsonSchema, BeforeValidator
from typing_extensions import Annotated

from constants.priority_mappings import priority_to_str, str_to_priority


def __to_enum(value):
    if isinstance(value, Priority):
        return value

    try:
        return str_to_priority[value]
    except:
        raise ValueError(f"expected: `{'`, `'.join(str_to_priority.keys())}`")


def __to_str(value):
    if isinstance(value, Priority):
        return priority_to_str[value]

    if value in str_to_priority.keys():
        return value

    if not (value and value.strip()):
        return None

    raise ValueError("invalid Priority for string conversion")


PriorityStr = Annotated[
    Priority,
    BeforeValidator(__to_enum),
    PlainSerializer(__to_str, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization'),
]
