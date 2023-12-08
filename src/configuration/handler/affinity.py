from typing import List, Optional

from pydantic import PlainSerializer, WithJsonSchema, BeforeValidator
from typing_extensions import Annotated

from util.cpu import parse_affinity, format_affinity


def __to_list(value) -> Optional[List[int]]:
    if isinstance(value, List):
        return value

    if not value.strip():
        return None

    return parse_affinity(value)


def __to_str(value) -> Optional[str]:
    if not value:
        return None

    if isinstance(value, List):
        return format_affinity(value)

    return value


Affinity = Annotated[
    Optional[List[int]],
    BeforeValidator(__to_list),
    PlainSerializer(__to_str, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization'),
]
