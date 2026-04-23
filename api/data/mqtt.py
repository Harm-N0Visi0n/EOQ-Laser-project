import paho.mqtt.client as paho

from data.gun import Gun
from data.unit import Unit
from data.module import Module
from data import data_lock, get_guns_dict, get_modules_dict, units, events


def connect(host: str):
    client.connect_async(host, 1883)
    client.loop_start()

    def on_connect(client: paho.Client, userdata, connect_flags, reason_code):  # noqa: ARG001
        print("🛜  MQTT server connected! 🛜", flush=True)
        client.publish("system/*/v1/identify")
        client.subscribe('#', qos=1)
    client.on_connect = on_connect
    client.on_connect_fail = lambda client, userdata: print("⚠️  MQTT server connect failed! ⚠️", flush=True)  # noqa: ARG005


def disconnect():
    client.disconnect()


# All the heavy lifting is in the on_message where all incoming messages from targets and guns
def on_message(client, userdata, msg):  # noqa: ARG001
    # Silly thing, but the payload is in bytes, howver we know it's a string --> small conversion needed
    msg.payload = msg.payload.decode("utf-8")
    msg.topic  # noqa: B018
    msg.payload  # noqa: B018
    split_topic = str(msg.topic).split("/")

    unit_type = split_topic[0] # module or gun
    is_unique = split_topic[1] != "*"
    identifier = int(split_topic[1], 0) if is_unique else 0
    version = split_topic[2]
    subtopic = split_topic[3]

    if version != "v1":
        print("Unsupported version topic!")
        return

    units_to_update: dict[int, Unit] = {}
    match unit_type:
        case "module":
            if is_unique:
                with data_lock:
                    units.setdefault(identifier, Module())
            units_to_update = get_modules_dict() # type: ignore
        case "gun":
            if is_unique:
                with data_lock:
                    units.setdefault(identifier, Gun())
            units_to_update = get_guns_dict() # type: ignore
        case _:
            print(f"⚠️ Unhandled message:\n\ttopic:\t{msg.topic}\n\t:payload:\t{msg.payload} ⚠️")
            return
    if is_unique:
        units_to_update = {identifier: units_to_update[identifier]}
        with data_lock:
            events.append((identifier, subtopic, msg.payload))

    for unit in units_to_update.values():
        is_message_handled = unit.handle_mqtt_message(identifier, subtopic, msg.payload)
        if not is_message_handled:
            print(f"⚠️ Unhandled message:\n\ttopic:\t{msg.topic}\n\t:payload:\t{msg.payload} ⚠️")
            return


def publish_data(identifier: str, unit: Unit, topic: str, value):
    if not client.is_connected():
        print("⚠️ Can't publish data. MQTT server not connected! ⚠️", flush=True)
        return
    
    unit_type = type(unit).__name__.lower()

    if topic not in unit.get_allowed_mqtt_topics():
        raise NotImplementedError(f"Can't publish data. Topic {topic} not implemented for unit type {unit_type}")
    
    print(f"{unit_type}/{identifier}/v1/{topic}")
    print(value)
    client.publish(f"{unit_type}/{identifier}/v1/{topic}", value)


client = paho.Client()
client.on_message = on_message
