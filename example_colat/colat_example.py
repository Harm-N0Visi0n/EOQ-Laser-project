#
# Trivial example of the messages between targets (modules) and guns.
#
# The concept is as follows:
# - All modules are initialized to RED
# - All guns are initialized with an ammo of 100
# - If a GUN hits a TARGET (aka module), the target's colour changes to GREEN
#
# All of this is handled with the MQTT message processor!
#

import paho.mqtt.client as paho
import time

MQTT_SERVER = 'localhost'

list_of_guns = set()
list_of_targets = set()

def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribe: "+str(mid)+" "+str(granted_qos))

#
# All the heavy lifting is in the on_message where all incoming messages from targets and guns
# will be processed. The best approach is to split this into individual functions so the code
# remains readable.
#
def on_message(client, userdata, msg):
    #
    # Silly thing, but the payload is in bytes, howver we know it's a string --> small conversion needed
    #
    msg.payload = msg.payload.decode("utf-8")

    #
    # Print the content to the terminal.
    #
    print(" >> message @ topic:"+msg.topic+" payload:"+str(msg.payload))

    #
    # The topic in the messages tells you who/what   gun/<gun-id>/v1/<topic>  or    module/<target-id>/v1/<topic>
    # So, an easy way to check for the contents, split the topic on all slashes, that gives the individual elements
    #
    split_elements = str(msg.topic).split("/")

    #
    # Now check the topic elements one by one and acts if necessary
    #
    if (split_elements[0] == "module"):
        #
        # Check if this a new target we have to remember
        #
        if (split_elements[1] != "*"):
            list_of_targets.add(split_elements[1])

        #
        # If the topic is 'hit', we know this target has been shot by a gun. The gun's PWM value is in the payload
        #
        if (split_elements[3].find("hit") != -1):
             print("Target has been hit by gun with pwm "+str(msg.payload)+" ! Let's mark the target GREEN :)")
             client.publish("module/"+target+"/v1/color", "0,1000,0,0")

    elif (split_elements[0] == "gun"):
        #
        # Check if this a new gun we have to remember
        #
        if (split_elements[1] != "*"):
            list_of_guns.add(split_elements[1])

        if (split_elements[3] == "fire-start"):
            print("Gun fired!")

#
# Initialize the MQTT client for receiving and sending messages to guns and targets
#
client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message

client.connect(MQTT_SERVER, 1883) # Dit moet uiteraard de u281nn-commandpost zijn!
client.subscribe('#', qos=1)

client.loop_start()

#
# Collect all guns and targets active on this server
# The trick is to use the GROUP indicator '*' instead of a gun's or target's unique identifier.
#
client.publish("module/*/v1/identify", "")
client.publish("gun/*/v1/identify", "")
print("Requesting all targets and guns to make them identify themselves...(takes 5 seconds)")
time.sleep(5)

#
# Print the current list of guns and targets on the screen so you can check if this matches what you expect
#
print("Guns: "+str(list_of_guns))
print("Targets: "+str(list_of_targets))

#
# Initialize all guns with a PWM and a ammo
#
pwm = 10
for gun in list_of_guns:
    client.publish("gun/"+gun+"/v1/ammo", "999")
    client.publish("gun/"+gun+"/v1/pwm", pwm)
    client.publish("gun/"+gun+"/v1/gun-id", pwm)
    pwm = pwm + 10

#
# Initalize all targets to RED
#
for target in list_of_targets:
    client.publish("module/"+target+"/v1/color", "100,0,0,0")

#
# Here starts the endless list where additional intelligence can be added. For now it's an empty forever-loop
#
while True:
    time.sleep(30)
