from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime, timedelta
import threading
import time

app = Flask(__name__)
alarm_time = None
alarm_triggered = False

def check_alarm():
    global alarm_time, alarm_triggered
    while True:
        if alarm_time:
            now = datetime.now().time()
            if now >= alarm_time and not alarm_triggered:
                alarm_triggered = True
                alarm_time = None
        time.sleep(1)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    global alarm_time, alarm_triggered
    data = request.get_json()
    alarm_time_str = data.get('time')
    if alarm_time_str:
        alarm_time = datetime.strptime(alarm_time_str, '%H:%M').time()
        alarm_triggered = False
        return jsonify({"message": f"Alarm set for {alarm_time_str}"}), 200
    return jsonify({"message": "Invalid time format"}), 400

@app.route('/check_alarm', methods=['GET'])
def check_alarm_status():
    return jsonify({"alarm": alarm_triggered})

@app.route('/stop_alarm', methods=['POST'])
def stop_alarm():
    global alarm_triggered
    alarm_triggered = False
    return jsonify({"message": "Alarm stopped"}), 200

@app.route('/snooze_alarm', methods=['POST'])
def snooze_alarm():
    global alarm_time, alarm_triggered
    alarm_triggered = False
    snooze_duration = timedelta(minutes=5)
    new_alarm_time = datetime.now() + snooze_duration
    alarm_time = new_alarm_time.time()
    return jsonify({"message": "Alarm snoozed for 5 minutes"}), 200

if __name__ == '__main__':
    threading.Thread(target=check_alarm, daemon=True).start()
    app.run(debug=True)

