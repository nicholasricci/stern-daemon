from flask_socketio import SocketIO
from flask_cors import CORS
from flask import Flask
from .views.oc import oc_blueprint
from .views.fs import fs_blueprint

socketio = SocketIO(logger=True, engineio_logger=True, cors_allowed_origins="*")
from . import stern_events


def create_app(config_filename):
    app = Flask(__name__)
    CORS(app, origins=["*"], allow_headers=["*"])
    app.config.from_pyfile(config_filename)

    app.register_blueprint(oc_blueprint, url_prefix='/api/oc')
    app.register_blueprint(fs_blueprint, url_prefix='/api/fs')

    # Inizializza Flask-SocketIO con l'app Flask
    socketio.init_app(app)

    return app
