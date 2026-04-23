from uuid import uuid4

from fastapi import APIRouter, WebSocket

from data.module import Module
from data.mqtt import publish_data
from routers.unit import check_none, get_all_identifiers, get_unit, get_unit_battery, get_unit_events, get_unit_version, get_unit_volume, set_unit_volume, websocket_events
from data import get_modules_dict
from schemas.battery import Battery
from schemas.color import Color
from schemas.version import Version
from schemas.volume import Volume


router = APIRouter(prefix="/module", tags=["🔮 Module"])


@router.get("/all")
def get_all() -> list[str]:
    return get_all_identifiers(get_modules_dict())


@router.get("/events")
def get_events() -> list[tuple[str, str, str]]:
    return get_unit_events(get_modules_dict())


@router.get("/{identifier}/battery")
def get_battery(identifier: str) -> Battery:
    return get_unit_battery(identifier, get_modules_dict())


@router.get("/{identifier}/volume")
def get_volume(identifier: str) -> Volume:
    return get_unit_volume(identifier, get_modules_dict())


@router.post("/{identifier}/volume")
def set_volume(identifier: str, value: Volume):
    return set_unit_volume(identifier, get_modules_dict(), value)


@router.get("/{identifier}/version")
def get_version(identifier: str) -> Version:
    return get_unit_version(identifier, get_modules_dict())


@router.get("/{identifier}/color")
def get_color(identifier: str) -> Color:
    module = check_none(get_unit(identifier, get_modules_dict()))
    assert isinstance(module, Module)
    return check_none(module.color)


@router.post("/{identifier}/color")
def set_color(identifier: str, color: Color):
    module = get_unit(identifier, get_modules_dict())
    assert isinstance(module, Module)
    module.color = color
    publish_data(identifier, module, "color", color.to_colat_format())


@router.websocket("/")
async def websocket(websocket: WebSocket):
    await websocket_events(websocket, uuid4(), "module")
