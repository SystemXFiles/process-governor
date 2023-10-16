from psutil._pswindows import Priority, IOPriority

from configuration.rule import Rule
from service.config_service import ConfigService

# voicemeeter8x64.exe
# voicemeeterclient.exe
# element.exe
# Audiodg.exe
# AudioSrv
# AudioEndpointBuilder

if __name__ == '__main__':
    config = ConfigService.load_config()

    config.rules = [
        Rule(
            processSelector="voicemeeter8x64.exe",
            priority=Priority.REALTIME_PRIORITY_CLASS,
            affinity="16-23"
        ),
        Rule(
            processSelector="voicemeeterclient.exe ",
            priority=Priority.REALTIME_PRIORITY_CLASS,
            affinity="16-23"
        ),
        Rule(
            processSelector="element.exe",
            priority=Priority.REALTIME_PRIORITY_CLASS,
            affinity="16-23"
        ),
        Rule(
            processSelector="Audiodg.exe",
            priority=Priority.REALTIME_PRIORITY_CLASS,
            affinity="16-23"
        ),
        Rule(
            serviceSelector="AudioSrv",
            priority=Priority.REALTIME_PRIORITY_CLASS,
            affinity="16-23"
        ),
        Rule(
            serviceSelector="AudioEndpointBuilder",
            priority=Priority.REALTIME_PRIORITY_CLASS,
            affinity="16-23"
        ),
        Rule(
            processSelector="*",
            affinity="0-15"
        )
    ]

    ConfigService.save_config(config)

