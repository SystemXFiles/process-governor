from psutil._pswindows import IOPriority
from pydantic import BeforeValidator, PlainSerializer, WithJsonSchema
from typing_extensions import Annotated

from constants.priority_mappings import iopriority_to_str, str_to_iopriority


def __to_enum(value):
    if isinstance(value, IOPriority):
        return value

    try:
        return str_to_iopriority[value]
    except:
        raise ValueError(f"expected: `{'`, `'.join(str_to_iopriority.keys())}`")


def __to_str(value):
    if isinstance(value, IOPriority):
        return iopriority_to_str[value]

    if value in str_to_iopriority.keys():
        return value

    if not (value and value.strip()):
        return None

    raise ValueError("invalid IOPriority for string conversion")


IOPriorityStr = Annotated[
    IOPriority,
    BeforeValidator(__to_enum),
    PlainSerializer(__to_str, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization'),
]
