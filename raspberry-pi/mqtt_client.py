import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883


def create_client():
    client = mqtt.Client()
    client.reconnect_delay_set(min_delay=1, max_delay=30)
    client.connect_async(MQTT_BROKER, MQTT_PORT)
    return client
