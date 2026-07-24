import json
import time

MQTT_TOPIC = "yard/moisture"


def setup_sensor(client, state):
    def on_connect(client, userdata, flags, rc):
        client.subscribe(MQTT_TOPIC)

    def on_message(client, userdata, msg):
        data = json.loads(msg.payload.decode())

        state.voltage = data["moisture"]
        state.last_reading_time = time.time()

        print(f"Voltage: {state.voltage}")

    client.on_connect = on_connect
    client.on_message = on_message
