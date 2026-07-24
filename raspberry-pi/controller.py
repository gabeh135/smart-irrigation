import time
from sensor import get_moisture
from sprinkler import emit_on, emit_off


DRY_THRESHOLD = 0.5
SATURATED_THRESHOLD = 1.5

MIN_WATER_TIME = 5 * 60
MAX_WATER_TIME = 30 * 60


def update(state):
    state.voltage = get_moisture()

    if not state.sprinkler_on:
        if state.voltage < DRY_THRESHOLD:
            emit_on(state)

    else:
        runtime = time.time() - state.sprinkler_start_time

        if runtime > MAX_WATER_TIME or (runtime > MIN_WATER_TIME and state.voltage > SATURATED_THRESHOLD):
            emit_off(state)
