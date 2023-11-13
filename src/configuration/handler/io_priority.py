from psutil._pswindows import IOPriority
from pydantic import BeforeValidator, PlainSerializer, WithJsonSchema
from typing_extensions import Annotated

from constants.priority_mappings import iopriority_to_str, str_to_iopriority


def __to_enum(value):
    if isinstance(value, IOPriority):
        return value
    return str_to_iopriority[value]


IOPriorityStr = Annotated[
    IOPriority,
    BeforeValidator(__to_enum),
    PlainSerializer(lambda value: iopriority_to_str[value], return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization'),
]
