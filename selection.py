import requests
import time

API_SERVER = '192.168.0.222'
modules = requests.get(f"http://{API_SERVER}:8000/module/all").json()
game_list = ['mexican_standoff.py', 'sequance.py']
connected_list = []
red = {
    "red": 255,
    "green": 0,
    "blue": 0,
    "white": 0,
    "twinkle": False,
}
green = {
    "red": 0,
    "green": 255,
    "blue": 0,
    "white": 0,
    "twinkle": False,
}
blue = {
    "red": 0,
    "green": 0,
    "blue": 255,
    "white": 0,
    "twinkle": False,
}
gold = {
    "red": 212,
    "green": 165,
    "blue": 55,
    "white": 0,
    "twinkle": False,
}
list_colours = [red, green, blue, gold]

for index, game in enumerate(game_list):
    requests.post(
        f"http://{API_SERVER}:8000/module/{modules[index]}/color",
        json=list_colours[index],
        headers={"accept": "application/json"},
    )
    connected_list.append([modules[index], game, index])

all_events = requests.get(f"http://{API_SERVER}:8000/module/events").json()
for event in all_events:
    event_id = (event[0], event[1])  # (module, event_type)
    if event[1] == "hit-1":
        for index in connected_list:
            if event[0] in connected_list[index]:

# match got_hit
#     case 0
