from asyncio import Queue
from typing import Any
from uuid import UUID
from fastapi import HTTPException, WebSocket
from fastapi.websockets import WebSocketState

from data import data_lock, int_to_hex_str, websocket_queues, events
from data.mqtt import publish_data
from data.unit import Unit
from schemas.volume import Volume


def get_unit(identifier: str, units: dict[int, Any]):
    result = units.get(int(identifier, 0))
    if result is None or not isinstance(result, Unit):
        raise HTTPException(404)
    return result


def check_none(value):
    if value is None:
        raise HTTPException(404)
    return value


def get_all_identifiers(units: dict[int, Any]):
    return [int_to_hex_str(identifier) for identifier in units]


def get_unit_events(units: dict[int, Any]) -> list[tuple[str, str, str]]:
    with data_lock:
        results = [event for event in events if event[0] in list(units)]
        for result in results:
            events.remove(result)
        return [(int_to_hex_str(result[0]), result[1], result[2]) for result in results]


def get_unit_battery(identifier: str, units: dict[int, Any]):
    return check_none(get_unit(identifier, units).battery)


def get_unit_volume(identifier: str, units: dict[int, Any]):
    return check_none(get_unit(identifier, units).volume)


def set_unit_volume(identifier: str, units: dict[int, Any], value: Volume):
    unit = get_unit(identifier, units)
    unit.volume = value
    publish_data(identifier, unit, "volume", value.level)


def get_unit_version(identifier: str, units: dict[int, Any]):
    unit = get_unit(identifier, units)
    return check_none(unit.version)


async def websocket_events(
        websocket: WebSocket,
        uuid: UUID,
        unit_type: str | None = None,
        identifier: str | None = None):

    websocket_queues[uuid] = Queue()
    await websocket.accept()
    with data_lock:
        queue = websocket_queues[uuid]
    while websocket.client_state == WebSocketState.CONNECTED:
        event = await queue.get()
        queue.task_done()
        if unit_type is not None and event[1] != unit_type:
            continue
        if identifier is not None and event[0] != int(identifier, 0):
            continue
        await websocket.send_json(event)
    with data_lock:
        del websocket_queues[uuid]
