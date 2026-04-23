from enum import StrEnum

from data.unit import Unit
from schemas.color import Color


class GunType(StrEnum):
    single_shot = 'single-shot'
    continuous_mode = 'continuous-mode'


class Gun(Unit):

    def __init__(self) -> None:
        super().__init__()
        self.type: GunType | None = None
        self.team_color: Color | None = None
        self.pwm: int | None = None
        self.ammo: int | None = None
        self.ammo_depletion: int | None = None

    @classmethod
    def get_allowed_mqtt_topics(cls) -> list[str]:
        return super().get_allowed_mqtt_topics() + [
            "gun-type",
            "pwm",
            "ammo",
            "ammo-depletion",
            "haptic-feedback",
            "text-message",
            "team-color"
        ]

    def handle_mqtt_message(self, identifier: int, subtopic: str, value: str) -> bool:
        if super().handle_mqtt_message(identifier, subtopic, value):
            return True
        
        match subtopic:
            case "team-color":
                colors = value.split(",")
                self.team_color = Color(
                    red=int(colors[0]),
                    green=int(colors[1]),
                    blue=int(colors[2]),
                    white=int(colors[3]) if len(colors) >= 4 else None,
                    twinkle=False
                )
            case "fire-start" | "fire-stop":
                from data import put_websocket_event  # noqa: PLC0415
                self.ammo = int(value)
                put_websocket_event(identifier, self, subtopic, self.ammo)
            case _:
                return False
        return True
