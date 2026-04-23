from asyncio import Queue
import os
from threading import Lock
from uuid import UUID

from data.unit import Unit
from data.gun import Gun
from data.module import Module


def parse_ids(env_var: str) -> list[int]:
    full_list = os.getenv(env_var, "")
    return [int(id.strip(), 0) for id in full_list.split(",") if id.strip()]


units: dict[int, Module | Gun] = {}

for id in parse_ids("REAL_GUNS"):
    units[id] = Gun()
for id in parse_ids("REAL_MODULES"):
    units[id] = Module()


events: list[tuple[int, str, str]] = [] # list[unit_identifier, event, value]
websocket_queues: dict[UUID, Queue[tuple[int, str, str, int]]] = {} # dict[socket_uuid, unhandled_evens[unit_identifier, type, event, value]]


data_lock = Lock()


def get_modules_dict():
    with data_lock:
        return {identifier: module for identifier, module in units.items() if isinstance(module, Module)}


def get_guns_dict():
    with data_lock:
        return {identifier: gun for identifier, gun in units.items() if isinstance(gun, Gun)}


def put_websocket_event(identifier: int, unit: Unit, subtopic: str, value: int):
    unit_type = type(unit).__name__.lower()
    with data_lock:
        for websocket_queue in websocket_queues.values():
            websocket_queue.put_nowait((identifier, unit_type, subtopic, value))


def int_to_hex_str(value: int) -> str:
    return f"0x{value:0{8}x}"
