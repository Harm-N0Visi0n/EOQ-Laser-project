import requests
import time
import random

modules = requests.get("http://localhost:8000/module/all").json()

list_modules = []
sequence_colour = {
    "red": 0,
    "green": 0,
    "blue": 255,
    "white": 0,
    "twinkle": False,
}
miss_colour = {
    "red": 255,
    "green": 0,
    "blue": 0,
    "white": 0,
    "twinkle": False,
}
correct_hit_colour = {
    "red": 0,
    "green": 255,
    "blue": 0,
    "white": 0,
    "twinkle": False,
}


def make_gray():
    for module in modules:
        payload = {
            "red": 0,
            "green": 0,
            "blue": 0,
            "white": 0,
            "twinkle": False,
        }
        list_modules.append(module)
        requests.post(
            f"http://localhost:8000/module/{module}/color",
            json=payload,
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
        )


def check_correct_hit(module_sequence):
    seen_events = set()
    index = 0
    
    while index < len(module_sequence):
        all_events = requests.get("http://localhost:8000/module/events").json()
        
        for event in all_events:
            event_id = (event[0], event[1])  # (module, event_type)
            
            if event[1] == "hit-1" and event_id not in seen_events:
                seen_events.add(event_id)
                
                if event[0] == module_sequence[index]:
                    requests.post(
                        f"http://localhost:8000/module/{event[0]}/color",
                        json=correct_hit_colour,
                        headers={"accept": "application/json"},
                    )
                    index += 1
                else:
                    return False  # Wrong module hit
        
        time.sleep(0.1)  # Small delay to avoid hammering the API
    
    return True


make_gray()
module_sequence = []
game_state = True
while game_state is True:
    rnd_number = random.choice(list_modules)
    module_sequence.append(rnd_number)
    for module in module_sequence:
        time.sleep(1)
        requests.post(
            f"http://localhost:8000/module/{module}/color",
            json=sequence_colour,
            headers={
                "accept": "application/json",
            },
        )
    game_state = check_correct_hit(module_sequence)
    time.sleep(2)
    make_gray()
