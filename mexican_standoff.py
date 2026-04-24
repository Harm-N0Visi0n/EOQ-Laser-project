import requests
import time
import random
API_SERVER = '192.168.0.222'
Hard_coded = ['0x004868cc', '0x0096bad0', '0x004856c4', '0x0097e770']
modules = requests.get(f"http://{API_SERVER}:8000/module/all").json()
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
sound = ""

green_list = []
red_list = []
player_sequence = []
list_modules = []


def make_gold():
    for module in modules: #modules
        list_modules.append(module)
        check = requests.post(
            f"http://{API_SERVER}:8000/module/{module}/color",
            json=gold,
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
        )


def randomize_modules():
    temp_list = list_modules.copy()
    one_or_zero = len(list_modules) % 2
    for _ in range(len(list_modules)// 2-one_or_zero):
        rnd = random.choice(temp_list)
        green_list.append(rnd)
        temp_list.remove(rnd)
        rnd = random.choice(temp_list)
        red_list.append(rnd)
        temp_list.remove(rnd)
        
        
def mexican_standoff_setup():
    make_gold()
    randomize_modules()
    time.sleep(5)
    for module in green_list:
        requests.post(
            f"http://{API_SERVER}:8000/module/{module}/color",
            json=green,
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
        )
    for module in red_list:
        requests.post(
            f"http://{API_SERVER}:8000/module/{module}/color",
            json=red,
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
        )


def check_correct_hit(list_green, list_red):
    seen_events = set()
    green_index = 0
    red_index = 0
    green_done = False
    red_done = False

    # Set all modules to their player colour at the start
    for module in list_green:
        requests.post(
            f"http://{API_SERVER}:8000/module/{module}/color",
            json=green,
            headers={"accept": "application/json"},
        )
    for module in list_red:
        requests.post(
            f"http://{API_SERVER}:8000/module/{module}/color",
            json=red,
            headers={"accept": "application/json"},
        )

    while not green_done and not red_done:
        all_events = requests.get(f"http://{API_SERVER}:8000/module/events").json()

        for event in all_events:
            event_id = (event[0], "hit", all_events.index(event))
            if not event[1].startswith("hit-") or event_id in seen_events:
                continue
            seen_events.add(event_id)

            module_hit = event[0]

            # Green player hit
            if not green_done and module_hit in list_green:
                if module_hit == list_green[green_index]:
                    # Correct — turn gold
                    requests.post(
                        f"http://{API_SERVER}:8000/module/{module_hit}/color",
                        json=gold,
                        headers={"accept": "application/json"},
                    )
                    green_index += 1
                    if green_index == len(list_green):
                        green_done = True
                else:
                    # Wrong — reset all green modules back to green
                    green_index = 0
                    seen_events.clear()
                    for module in list_green:
                        requests.post(
                            f"http://{API_SERVER}:8000/module/{module}/color",
                            json=green,
                            headers={"accept": "application/json"},
                        )
                    break

            # Red player hit
            elif not red_done and module_hit in list_red:
                if module_hit == list_red[red_index]:
                    # Correct — turn gold
                    requests.post(
                        f"http://{API_SERVER}:8000/module/{module_hit}/color",
                        json=gold,
                        headers={"accept": "application/json"},
                    )
                    red_index += 1
                    if red_index == len(list_red):
                        red_done = True
                else:
                    # Wrong — reset all red modules back to red
                    red_index = 0
                    seen_events.clear()
                    for module in list_red:
                        requests.post(
                            f"http://{API_SERVER}:8000/module/{module}/color",
                            json=red,
                            headers={"accept": "application/json"},
                        )
                    break

        time.sleep(0.1)

    if green_done:
        print("Green player wins!")
        return "green"
    else:
        print("Red player wins!")
        return "red"


def main():
    mexican_standoff_setup()
    game_state = True
    while game_state is True:
        time.sleep(0.1)
        check_correct_hit(green_list, red_list)


main()
