from psutil._pswindows import Priority, IOPriority

from configuration.rule import Rule
from service.config_service import ConfigService

if __name__ == '__main__':
    config = ConfigService.load_config()

    config.rules = [
        Rule(
            processSelector="example.exe",
            priority=Priority.HIGH_PRIORITY_CLASS,
            ioPriority=IOPriority.IOPRIO_NORMAL,
            affinity="1;3-5"
        ),
        Rule(
            serviceSelector="Audio*",
            priority=Priority.REALTIME_PRIORITY_CLASS,
            ioPriority=IOPriority.IOPRIO_HIGH,
            affinity="0;2;4"
        ),
    ]

    ConfigService.save_config(config)
