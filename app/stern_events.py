from subprocess import Popen, PIPE
from flask_socketio import emit
from . import socketio

process = None

@socketio.on('start_log_stream')
def handle_log_stream(data):
    deployment_name = data['deployment_name']
    command = f"stern {deployment_name} --timestamps"
    process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            emit('log_stream', {'data': output.strip()})

@socketio.on('stop_log_stream')
def handle_log_stream():
    if process:
        process.kill()
        process = None