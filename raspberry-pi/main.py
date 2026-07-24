import threading
import time

from model import SystemState
from controller import update
from dashboard import create_dashboard
from mqtt_client import create_client
from sensor import setup_sensor


state = SystemState()


def controller_loop():
    while True:
        update(state)
        time.sleep(1)


mqtt_client = create_client()

setup_sensor(mqtt_client, state)

mqtt_client.loop_start()


threading.Thread(
    target=controller_loop,
    daemon=True
).start()


create_dashboard(state)
