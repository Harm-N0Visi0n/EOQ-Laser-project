from datetime import datetime

from schemas.battery import Battery
from schemas.version import Version
from schemas.volume import Volume


class Unit:

    def __init__(self) -> None:
        self.volume: Volume | None = None
        self.battery: Battery | None = None
        self.version: Version | None = None

    @classmethod
    def get_allowed_mqtt_topics(cls) -> list[str]:
        return ["volume"]

    def handle_mqtt_message(self, identifier: int, subtopic: str, value: str) -> bool:  # noqa: ARG002
        from data import put_websocket_event  # noqa: PLC0415
        match subtopic: # type: ignore
            case "present":
                pass
            case "volume":
                self.volume = Volume(level=int(value))
            case "battery-level":
                self.battery = Battery(level=float(value.split(" V", maxsplit=1)[0]))
            case "version":
                version = value.split(" - ")
                self.version = Version(
                    version=version[0],
                    date=datetime.fromisoformat(version[1])
                )
            case _:
                return False
        return True
