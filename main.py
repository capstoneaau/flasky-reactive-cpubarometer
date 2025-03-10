import time
import psutil
from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BeWareOfTheManWhoSpeaksInHands'
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*")

def get_cpu_temperature():
    temperatures = psutil.sensors_temperatures()
    sensor = None
    if temperatures['coretemp'] is None:
        if temperatures['cpu_thermal'] is None:
            return "Platform not supported"
        sensor = 'cpu_thermal'
    sensor = 'coretemp'
    cpu_temperatures = temperatures[sensor][0]  # Assuming coretemp is the sensor name
    return cpu_temperatures.current

@app.route("/")
def get():
    return f"<b>Current CPU temp (static): {get_cpu_temperature()}</b>"

def background_task():
    while True:
        temp = get_cpu_temperature()
        socketio.emit('data', {'data': temp})
        time.sleep(1)

if __name__ == '__main__':
    socketio.start_background_task(background_task)
    socketio.run(app, debug=True,port=5000)
