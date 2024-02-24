from flask import Blueprint, jsonify, request
import json
import os

fs_blueprint = Blueprint('fs', __name__)


def get_home_directory():
    return os.path.expanduser("~")


def get_configs_directory():
    configs_directory = get_home_directory() + '/.stern-gui'
    os.makedirs(configs_directory, exist_ok=True)
    return configs_directory


def get_configs_file_name():
    return get_configs_directory() + '/configs.json'


def read_configs():
    configs_file = get_configs_file_name()
    if os.path.exists(configs_file):
        with open(configs_file, 'r') as file:
            return json.load(file)
    return None


def write_configs(configs):
    configs_file = get_configs_file_name()
    with open(configs_file, 'w') as file:
        json.dump(configs, file)


@fs_blueprint.route('/configs', methods=['POST'])
def set_configs():
    data = request.json
    write_configs(data)
    return data


@fs_blueprint.route('/configs', methods=['GET'])
def get_configs():
    data = read_configs()
    if data:
        return data
    return jsonify(), 204
