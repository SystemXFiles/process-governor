from psutil._pswindows import Priority
from pydantic import PlainSerializer, WithJsonSchema, BeforeValidator
from typing_extensions import Annotated

__priority_to_str_mapping = {
    Priority.ABOVE_NORMAL_PRIORITY_CLASS: 'AboveNormal',
    Priority.BELOW_NORMAL_PRIORITY_CLASS: 'BelowNormal',
    Priority.HIGH_PRIORITY_CLASS: 'High',
    Priority.IDLE_PRIORITY_CLASS: 'Idle',
    Priority.NORMAL_PRIORITY_CLASS: 'Normal',
    Priority.REALTIME_PRIORITY_CLASS: 'Realtime',
}

__str_to_priority_mapping = {
    'AboveNormal': Priority.ABOVE_NORMAL_PRIORITY_CLASS,
    'BelowNormal': Priority.BELOW_NORMAL_PRIORITY_CLASS,
    'High': Priority.HIGH_PRIORITY_CLASS,
    'Idle': Priority.IDLE_PRIORITY_CLASS,
    'Normal': Priority.NORMAL_PRIORITY_CLASS,
    'Realtime': Priority.REALTIME_PRIORITY_CLASS,
}


def __to_enum(value):
    if isinstance(value, Priority):
        return value
    return __str_to_priority_mapping.get(value)


PriorityStr = Annotated[
    Priority,
    BeforeValidator(__to_enum),
    PlainSerializer(lambda value: __priority_to_str_mapping.get(value), return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization'),
]


def priority_to_str(value: Priority):
    """
    Convert a priority value to its corresponding string representation.

    Args:
        value (int): The priority value to convert.

    Returns:
        str: The string representation of the priority value, or None if no
            mapping is found.
    """
    return __priority_to_str_mapping.get(value)
