from jsonpickle.handlers import BaseHandler
from psutil._pswindows import Priority


class PriorityHandler(BaseHandler):
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

    def flatten(self, value: Priority, data):
        data['value'] = self.__priority_to_str_mapping[value]
        return data

    def restore(self, data) -> Priority:
        return self.__str_to_priority_mapping[data['value']]
