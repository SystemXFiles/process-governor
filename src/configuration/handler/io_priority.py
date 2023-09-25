from jsonpickle.handlers import BaseHandler
from psutil._pswindows import IOPriority


class IoPriorityHandler(BaseHandler):
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

    def flatten(self, value: IOPriority, data):
        data['value'] = self.__iopriority_to_str_mapping[value]
        return data

    def restore(self, data) -> IOPriority:
        return self.__str_to_iopriority_mapping[data['value']]
