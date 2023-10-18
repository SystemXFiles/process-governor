from psutil._pswindows import IOPriority
from pydantic import BeforeValidator, PlainSerializer, WithJsonSchema
from typing_extensions import Annotated

__iopriority_to_str_mapping = {
    IOPriority.IOPRIO_VERYLOW: 'VeryLow',
    IOPriority.IOPRIO_LOW: 'Low',
    IOPriority.IOPRIO_NORMAL: 'Normal',
    IOPriority.IOPRIO_HIGH: 'High',
}

__str_to_iopriority_mapping = {
    'VeryLow': IOPriority.IOPRIO_VERYLOW,
    'Low': IOPriority.IOPRIO_LOW,
    'Normal': IOPriority.IOPRIO_NORMAL,
    'High': IOPriority.IOPRIO_HIGH,
}


def __to_enum(value):
    if isinstance(value, IOPriority):
        return value
    return __str_to_iopriority_mapping.get(value)


IOPriorityStr = Annotated[
    IOPriority,
    BeforeValidator(__to_enum),
    PlainSerializer(lambda value: __iopriority_to_str_mapping.get(value), return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization'),
]


def iopriority_to_str(value: IOPriority):
    """
    Convert a IO priority value to its corresponding string representation.

    Args:
        value (int): The IO priority value to convert.

    Returns:
        str: The string representation of the IO priority value, or None if no
            mapping is found.
    """
    return __iopriority_to_str_mapping.get(value)
