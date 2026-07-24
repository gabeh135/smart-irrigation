import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"


def create_client():
    client = mqtt.Client()
    client.connect(MQTT_BROKER, 1883)
    return client
