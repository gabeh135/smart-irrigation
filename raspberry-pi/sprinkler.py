import time
from gpiozero import LED

status_led = LED(23)

def emit_on(state):
    if not state.sprinkler_on:
        print("EMIT ON")
        status_led.on()
        state.sprinkler_on = True
        state.sprinkler_start_time = time.time()


def emit_off(state):
    if state.sprinkler_on:
        print("EMIT OFF")
        status_led.off()
        state.sprinkler_on = False
        state.sprinkler_start_time = None
