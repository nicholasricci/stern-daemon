# run.py
from app import create_app, socketio

app = create_app('config.py')

if __name__ == '__main__':
    socketio.run(app)
