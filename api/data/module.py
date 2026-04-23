import random

from data.unit import Unit
from schemas.color import Color


class Module(Unit):
    
    def __init__(self) -> None:
        super().__init__()
        self.color: Color | None = None
        self.pwm_hit: int | None = None

    @classmethod
    def get_allowed_mqtt_topics(cls) -> list[str]:
        return super().get_allowed_mqtt_topics() + [
            "color",
            "hit",
            "hit-1",
            "hit-2",
            "hit-3",
            "hit-4",
            "hit-5",
            "hit-6"
        ]

    def handle_mqtt_message(self, identifier: int, subtopic: str, value: str) -> bool:
        if super().handle_mqtt_message(identifier, subtopic, value):
            return True
        
        match subtopic:
            case "color":
                colors = value.split(",")
                self.color = Color(
                    red=int(colors[0]),
                    green=int(colors[1]),
                    blue=int(colors[2]),
                    white=int(colors[3]) if len(colors) >= 4 else 0,
                    twinkle=len(colors) >= 5
                )
            case "hit" | "hit-1" | "hit-2" | "hit-3" | "hit-4" | "hit-5" | "hit-6":
                from data import put_websocket_event  # noqa: PLC0415
                self.pwm_hit = int(value)
                put_websocket_event(identifier, self, subtopic, self.pwm_hit)
            case _:
                return False
        return True
