from flask import Flask, redirect
import time

from sprinkler import emit_on, emit_off


app = Flask(__name__)

state = None


@app.route("/")
def index():

    runtime = 0

    if state.sprinkler_on:
        runtime = int(time.time() - state.sprinkler_start_time)

    return f"""
    <html>
    <head>
        <title>Soil Moisture Controller</title>
        <meta http-equiv="refresh" content="2">
    </head>

    <body>

    <h1>Soil Moisture Controller</h1>

    <h2>Voltage: {state.voltage:.3f} V</h2>

    <h2>
    Sprinkler:
    {"ON" if state.sprinkler_on else "OFF"}
    </h2>

    <h2>
    Runtime: {runtime} seconds
    </h2>

    <form action="/on">
        <button>Turn ON</button>
    </form>

    <form action="/off">
        <button>Turn OFF</button>
    </form>

    </body>
    </html>
    """


@app.route("/on")
def turn_on():

    emit_on(state)

    return redirect("/")


@app.route("/off")
def turn_off():

    emit_off(state)

    return redirect("/")


def create_dashboard(system_state):

    global state
    state = system_state

    app.run(
        host="0.0.0.0",
        port=5000
    )
