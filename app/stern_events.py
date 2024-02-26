from subprocess import Popen, PIPE
from flask_socketio import emit
import ptyprocess
import re
from . import socketio

process = None


@socketio.on('start_log_stream', namespace='/socket.io')
def handle_log_stream(data):
    deployment_name = data['deployment_name']
    filters = data['filters']
    command = f"stern {deployment_name} --timestamps"
    if filters.strip():
        command += f" {filters}"
    global process
    # process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)
    process = ptyprocess.PtyProcess.spawn(['bash', '-c', command])

    while True:
        # output = process.stdout.readline()
        output = process.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            text = str(output)
            text = text.replace("b'", "", 1)
            # remove the last character of the string
            text = text[:-5]
            #text = text.replace("\\r\\n'", "", 1)
            #text = re.sub(r'\\\\', r'\\', text)
            emit('log_stream', {'data': text})


@socketio.on('stop_log_stream', namespace='/socket.io')
def handle_log_stream():
    global process
    if process:
        # process.kill()
        process.terminate()
        process = None
