from psutil._pswindows import Priority
from pydantic import PlainSerializer, WithJsonSchema, BeforeValidator
from typing_extensions import Annotated

from constants.priority_mappings import priority_to_str, str_to_priority


def __to_enum(value):
    if isinstance(value, Priority):
        return value
    return str_to_priority[value]


PriorityStr = Annotated[
    Priority,
    BeforeValidator(__to_enum),
    PlainSerializer(lambda value: priority_to_str[value], return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization'),
]
