from flask import Flask, jsonify, request
from random import randrange
from datetime import datetime

app = Flask(__name__)

MAX_COLOR_CODE = 255
COLORS_LISTS = ["YELLOW", "RED", "PURPLE", "GREEN", "BLUE","MAGENTA"]
RUNNING_SERVERS = 0
MAX_SERVERS = 100


def generate_output(request_data,computation="report", count=0):
    global RUNNING_SERVERS
    result = dict()
    if computation == "start":
        RUNNING_SERVERS += count    
    elif computation == "stop":
        RUNNING_SERVERS -= count
    else:
        pass
    result["number_of_servers"] = RUNNING_SERVERS
    program_time = request_data['program_time']
    result["hour_hand_color"] = request_data['hour_hand_color']
    result["wall_color"] = request_data['wall_color']
    result["clock_face_color"] = request_data['clock_face_color']
    result["actual_time"] = datetime.now().strftime('%H:%M:%S')
    result["display_message"] = f"{program_time} -{computation} {count} servers"
    return jsonify(result)

@app.route('/')
def home():
    return 'Welcome<br> Go to:<br><b>/start</b> - to start servers<br> <b>/stop</b> - to stop servers<br><b>/report</b> - to generate report'

@app.route('/start', methods=["POST"])
def start_servers():
    request_data = None
    if request.method == 'POST':
        request_data = request.get_json()
        
    started_servers = randrange(MAX_SERVERS)
    return generate_output(request_data,computation="start",count=started_servers)

@app.route('/stop', methods=['POST'])
def stop_servers():
    request_data = None
    if request.method == 'POST':
        request_data = request.get_json()
    stopped_servers = randrange(RUNNING_SERVERS)
    return generate_output(request_data, computation="stop",count=stopped_servers)

@app.route('/report', methods=['POST'])
def report():
    request_data = None
    if request.method == 'POST':
        request_data = request.get_json()
    return generate_output(request_data)

app.run()