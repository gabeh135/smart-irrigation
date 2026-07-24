import threading
import time

from model import SystemState
from controller import update
from dashboard import create_dashboard


state = SystemState()


def controller_loop():
    while True:
        update(state)
        time.sleep(1)


threading.Thread(
    target=controller_loop,
    daemon=True
).start()


create_dashboard(state)
