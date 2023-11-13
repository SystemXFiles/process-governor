from typing import Final

from psutil._pswindows import IOPriority, Priority


class IOPriorityStr:
    VERYLOW: Final[str] = 'VeryLow'
    LOW: Final[str] = 'Low'
    NORMAL: Final[str] = 'Normal'
    HIGH: Final[str] = 'High'


iopriority_to_str: Final[dict] = {
    IOPriority.IOPRIO_VERYLOW: IOPriorityStr.VERYLOW,
    IOPriority.IOPRIO_LOW: IOPriorityStr.LOW,
    IOPriority.IOPRIO_NORMAL: IOPriorityStr.NORMAL,
    IOPriority.IOPRIO_HIGH: IOPriorityStr.HIGH,
}

str_to_iopriority: Final[dict] = {
    IOPriorityStr.VERYLOW: IOPriority.IOPRIO_VERYLOW,
    IOPriorityStr.LOW: IOPriority.IOPRIO_LOW,
    IOPriorityStr.NORMAL: IOPriority.IOPRIO_NORMAL,
    IOPriorityStr.HIGH: IOPriority.IOPRIO_HIGH,
}


class PriorityStr:
    ABOVE_NORMAL: Final[str] = 'AboveNormal'
    BELOW_NORMAL: Final[str] = 'BelowNormal'
    HIGH: Final[str] = 'High'
    IDLE: Final[str] = 'Idle'
    NORMAL: Final[str] = 'Normal'
    REALTIME: Final[str] = 'Realtime'


priority_to_str: Final[dict] = {
    Priority.ABOVE_NORMAL_PRIORITY_CLASS: PriorityStr.ABOVE_NORMAL,
    Priority.BELOW_NORMAL_PRIORITY_CLASS: PriorityStr.BELOW_NORMAL,
    Priority.HIGH_PRIORITY_CLASS: PriorityStr.HIGH,
    Priority.IDLE_PRIORITY_CLASS: PriorityStr.IDLE,
    Priority.NORMAL_PRIORITY_CLASS: PriorityStr.NORMAL,
    Priority.REALTIME_PRIORITY_CLASS: PriorityStr.REALTIME,
}

str_to_priority: Final[dict] = {
    PriorityStr.ABOVE_NORMAL: Priority.ABOVE_NORMAL_PRIORITY_CLASS,
    PriorityStr.BELOW_NORMAL: Priority.BELOW_NORMAL_PRIORITY_CLASS,
    PriorityStr.HIGH: Priority.HIGH_PRIORITY_CLASS,
    PriorityStr.IDLE: Priority.IDLE_PRIORITY_CLASS,
    PriorityStr.NORMAL: Priority.NORMAL_PRIORITY_CLASS,
    PriorityStr.REALTIME: Priority.REALTIME_PRIORITY_CLASS,
}
