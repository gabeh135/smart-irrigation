import time
from sprinkler import emit_on, emit_off


DRY_THRESHOLD = 0.5
SATURATED_THRESHOLD = 1.5

MIN_WATER_TIME = 5 * 60
MAX_WATER_TIME = 30 * 60

STALE_READING_TIMEOUT = 3 * 60


def update(state):
    if state.last_reading_time is None or time.time() - state.last_reading_time > STALE_READING_TIMEOUT:
        if state.sprinkler_on:
            emit_off(state)
        return

    if not state.sprinkler_on:
        if state.voltage < DRY_THRESHOLD:
            emit_on(state)

    else:
        runtime = time.time() - state.sprinkler_start_time

        if runtime > MAX_WATER_TIME:
            emit_off(state)

        elif runtime > MIN_WATER_TIME and state.voltage > SATURATED_THRESHOLD:
            emit_off(state)
