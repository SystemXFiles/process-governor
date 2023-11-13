from enum import Enum


class ProcessParameter(Enum):
    AFFINITY = "affinity"
    NICE = "nice"
    IONICE = "ionice"

    def __str__(self):
        return self.value
