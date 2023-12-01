from typing import Optional

from pydantic import BaseModel, Field

from configuration.handler.affinity import Affinity
from configuration.handler.io_priority import IOPriorityStr
from configuration.handler.priority import PriorityStr


class Rule(BaseModel):
    processSelector: Optional[str] = Field(
        default=None,
        title="Process Selector",
        description="Specifies the __name or pattern__ of the __process__ to which this rule applies.\n\n"
                    "**Supports wildcards:** `\*` (matches any characters) and `?` (matches any single character).\n"
                    "**Examples:** `name.exe` or `logioptionsplus_*.exe`."
    )

    serviceSelector: Optional[str] = Field(
        default=None,
        title="Service Selector",
        description="Specifies the __name or pattern__ of the __service__ to which this rule applies.\n\n"
                    "**Supports wildcards:** `\*` (matches any characters) and `?` (matches any single character).\n"
                    "**Examples:** `ServiceName` or `Audio*`."
    )

    priority: Optional[PriorityStr] = Field(
        default=None,
        title="Priority",
        description="Sets the **priority level** for the __process or service__.\n"
                    "Higher priority tasks are allocated more CPU time compared to lower priority tasks."
    )

    ioPriority: Optional[IOPriorityStr] = Field(
        default=None,
        title="I/O Priority",
        description="Sets the **I/O priority** for the __process or service__.\n"
                    "Higher I/O priority means more disk resources and better I/O performance."
    )

    affinity: Optional[Affinity] = Field(
        default=None,
        title="Affinity",
        description="Sets the **CPU core affinity** for the __process or service__, "
                    "defining which CPU cores are allowed for execution.\n\n"
                    "**Format:** range `1-4`, specific cores `0;2;4`, combination `1;3-5`."
    )
