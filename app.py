from flask import Flask, json, jsonify, request
from random import randrange
from datetime import datetime
import os

app = Flask(__name__)

env_config = os.getenv("APP_SETTINGS", "config.ProductionConfig")
app.config.from_object(env_config)

RUNNING_SERVERS = 0
RESULTS_LIST = list()


def generate_output(request_data,computation="report", count=0):
    global RUNNING_SERVERS, RESULTS_LIST
    result = dict()
    if computation == "start":
        RUNNING_SERVERS += count    
    elif computation == "stop":
        RUNNING_SERVERS -= count
    else:
        pass
    result["number_of_servers"] = RUNNING_SERVERS
    program_time = request_data['program_time']
    result["program_time"]=program_time
    result["hour_hand_color"] = request_data['hour_hand_color']
    result["wall_color"] = request_data['wall_color']
    result["clock_face_color"] = request_data['clock_face_color']
    result["actual_time"] = datetime.now().strftime('%H:%M:%S')
    
    if computation=="running":
        result["event"]="REPORT" 
        result["display_message"] = f"{program_time} - report {RUNNING_SERVERS} servers {computation}"
        result["message"]=f"Report {RUNNING_SERVERS} servers {computation}"
    else:
        result["event"]=computation 
        result["message"]=f"{computation} {count} servers"
        result["display_message"] = f"{program_time} - {computation} {count} servers"

    RESULTS_LIST.append(result)
    return jsonify(result)

@app.route('/')
def home():
    return 'Welcome<br> Go to:<br><b>/start</b> - to start servers<br> <b>/stop</b> - to stop servers<br><b>/report</b> - to generate report'

@app.route('/start', methods=["POST"])
def start_servers():
    request_data = None
    if request.method == 'POST':
        request_data = request.get_json()
        
    started_servers = randrange(10,20)
    return generate_output(request_data,computation="start",count=started_servers)

@app.route('/stop', methods=['POST'])
def stop_servers():
    request_data = None
    if request.method == 'POST':
        request_data = request.get_json()
        if(5>RUNNING_SERVERS):
            stopped_servers = randrange(RUNNING_SERVERS,5)
        else:
            stopped_servers = randrange(5,RUNNING_SERVERS)
   
    return generate_output(request_data, computation="stop",count=stopped_servers)

@app.route('/report', methods=['POST'])
def report():
    request_data = None
    if request.method == 'POST':
        request_data = request.get_json()
    return generate_output(request_data, computation="running") 

@app.route('/samplereport', methods=['GET'])
def sample_report():
    return jsonify(RESULTS_LIST)

@app.route('/clear', methods=['GET'])
def clear_list():
    RUNNING_SERVERS=0
    RESULTS_LIST.clear()
    return jsonify(RESULTS_LIST)

app.run()
