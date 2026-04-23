from uuid import uuid4

from fastapi import APIRouter, WebSocket

from data.gun import Gun, GunType
from data.mqtt import publish_data
from routers.unit import check_none, get_all_identifiers, get_unit_events, get_unit, get_unit_battery, get_unit_version, get_unit_volume, set_unit_volume, websocket_events
from data import get_guns_dict
from schemas.battery import Battery
from schemas.color import Color
from schemas.version import Version
from schemas.volume import Volume


router = APIRouter(prefix="/gun", tags=["🔫 Gun"])


@router.get("/all")
def get_all() -> list[str]:
    return get_all_identifiers(get_guns_dict())


@router.get("/events")
def get_events() -> list[tuple[str, str, str]]:
    return get_unit_events(get_guns_dict())


@router.get("/{identifier}/battery")
def get_battery(identifier: str) -> Battery:
    return get_unit_battery(identifier, get_guns_dict())


@router.get("/{identifier}/volume")
def get_volume(identifier: str) -> Volume:
    return get_unit_volume(identifier, get_guns_dict())


@router.post("/{identifier}/volume")
def set_volume(identifier: str, value: Volume):
    return set_unit_volume(identifier, get_guns_dict(), value)


@router.get("/{identifier}/version")
def get_version(identifier: str) -> Version:
    return get_unit_version(identifier, get_guns_dict())


@router.get("/{identifier}/gun-type")
def get_gun_type(identifier: str) -> GunType:
    gun = get_unit(identifier, get_guns_dict())
    assert isinstance(gun, Gun)
    return check_none(gun.type)


@router.post("/{identifier}/gun-type")
def set_gun_type(identifier: str, value: GunType):
    gun = get_unit(identifier, get_guns_dict())
    assert isinstance(gun, Gun)
    gun.type = value
    publish_data(identifier, gun, "gun-type", value)


@router.get("/{identifier}/ammo")
def get_ammo(identifier: str) -> int:
    gun = get_unit(identifier, get_guns_dict())
    assert isinstance(gun, Gun)
    return check_none(gun.ammo)


@router.get("/{identifier}/pwm")
def get_pwm(identifier: str) -> int:
    gun = get_unit(identifier, get_guns_dict())
    assert isinstance(gun, Gun)
    return check_none(gun.pwm)


@router.post("/{identifier}/pwm")
def set_pwm(identifier: str, value: int):
    gun = get_unit(identifier, get_guns_dict())
    assert isinstance(gun, Gun)
    assert 0 <= value <= 100
    gun.pwm = value
    publish_data(identifier, gun, "pwm", value)


@router.get("/{identifier}/ammo-depletion")
def get_ammo_depletion(identifier: str) -> int:
    gun = get_unit(identifier, get_guns_dict())
    assert isinstance(gun, Gun)
    return check_none(gun.ammo_depletion)


@router.post("/{identifier}/ammo-depletion")
def set_ammo_depletion(identifier: str, value: int):
    gun = get_unit(identifier, get_guns_dict())
    assert isinstance(gun, Gun)
    gun.ammo_depletion = value
    publish_data(identifier, gun, "ammo-depletion", value)


@router.post("/{identifier}/haptic-feedback")
def set_haptic_feedback(identifier: str, value: str):
    gun = get_unit(identifier, get_guns_dict())
    publish_data(identifier, gun, "haptic-feedback", value)


@router.post("/{identifier}/text-message")
def set_text_message(identifier: str, value: str):
    gun = get_unit(identifier, get_guns_dict())
    publish_data(identifier, gun, "text-message", value)


@router.get("/{identifier}/team-color")
def get_team_color(identifier: str) -> Color:
    gun = get_unit(identifier, get_guns_dict())
    assert isinstance(gun, Gun)
    return check_none(gun.team_color)


@router.post("/{identifier}/team-color")
def set_team_color(identifier: str, value: Color):
    gun = get_unit(identifier, get_guns_dict())
    assert isinstance(gun, Gun)
    gun.team_color = value
    publish_data(identifier, gun, "team-color", value.to_colat_format())


@router.websocket("/")
async def websocket(websocket: WebSocket):
    await websocket_events(websocket, uuid4(), "gun")
