import json

MQTT_TOPIC = "yard/moisture"


def setup_sensor(client, state):
    def on_message(client, userdata, msg):
        data = json.loads(msg.payload.decode())

        state.voltage = data["moisture"]

        print(f"Voltage: {state.voltage}")

    client.on_message = on_message
    client.subscribe(MQTT_TOPIC)
