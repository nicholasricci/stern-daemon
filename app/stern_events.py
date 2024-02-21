from subprocess import Popen, PIPE
from flask_socketio import emit
from . import socketio

process = None

@socketio.on('start_log_stream')
def handle_log_stream(data):
    deployment_name = data['deployment_name']
    filters = data['filters']
    command = f"stern {deployment_name} --timestamps"
    if filters.strip():
        command += f" {filters}"
    global process
    process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            emit('log_stream', {'data': output.strip()})

@socketio.on('stop_log_stream')
def handle_log_stream():
    global process
    if process:
        process.kill()
        process = None