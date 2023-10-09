from psutil._pswindows import Priority, IOPriority

from configuration.rule import Rule
from service.config_service import ConfigService

if __name__ == '__main__':
    config = ConfigService.load_config()

    config.rules = [
        Rule(processSelector="aida_bench64.dll"),
        Rule(
            processSelector="logioptionsplus_*.exe",
            priority=Priority.IDLE_PRIORITY_CLASS
        ),
        Rule(
            processSelector="cc_engine_x64.exe",
            priority=Priority.IDLE_PRIORITY_CLASS
        ),
        Rule(
            processSelector="starfield.exe",
            priority=Priority.IDLE_PRIORITY_CLASS,
            affinity="1-15;17;19;21;23"
        ),
        Rule(
            processSelector="qbittorrent.exe",
            priority=Priority.BELOW_NORMAL_PRIORITY_CLASS
        ),
        Rule(
            processSelector="discord.exe",
            priority=Priority.NORMAL_PRIORITY_CLASS
        ),
        Rule(
            processSelector="anydesk.exe",
            priority=Priority.NORMAL_PRIORITY_CLASS
        ),
        Rule(
            processSelector="aimp.exe",
            priority=Priority.HIGH_PRIORITY_CLASS,
            affinity="16-23"
        ),
        Rule(
            processSelector="audiodg.exe",
            priority=Priority.REALTIME_PRIORITY_CLASS,
            ioPriority=IOPriority.IOPRIO_HIGH,
            affinity="16-23"
        ),
        Rule(
            processSelector="element.exe",
            priority=Priority.REALTIME_PRIORITY_CLASS,
            ioPriority=IOPriority.IOPRIO_HIGH,
            affinity="16-23"
        ),
        Rule(
            processSelector="voicemeeter8x64.exe",
            priority=Priority.REALTIME_PRIORITY_CLASS,
            ioPriority=IOPriority.IOPRIO_HIGH,
            affinity="16-23"
        ),
        Rule(
            processSelector="voicemeeterclient.exe",
            priority=Priority.REALTIME_PRIORITY_CLASS,
            ioPriority=IOPriority.IOPRIO_HIGH,
            affinity="16-23"
        ),
        Rule(
            serviceSelector="*audio*",
            priority=Priority.REALTIME_PRIORITY_CLASS,
            ioPriority=IOPriority.IOPRIO_HIGH,
            affinity=""
        ),
        Rule(processSelector="*", affinity="0-15")
    ]

    ConfigService.save_config(config)
