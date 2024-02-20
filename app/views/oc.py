from flask import Blueprint, jsonify, request
from subprocess import Popen, PIPE

oc_blueprint = Blueprint('oc', __name__)


def run_oc_command(command):
    process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        return stdout.decode('utf-8')
    else:
        return f"Error: {stderr.decode('utf-8')}"

@oc_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    result = run_oc_command(f"oc login -u {data['email']} -p {data['password']} --server={data['server']}")
    return jsonify({"current_project": result.strip()})

@oc_blueprint.route('/current-project', methods=['GET'])
def current_project():
    result = run_oc_command("oc project -q")
    user_not_logged = result.lower().startswith("error")
    if user_not_logged:
        return jsonify({"current_project": "Not logged in"}), 401
    return jsonify({"current_project": result.strip()})

@oc_blueprint.route('/projects', methods=['GET'])
def projects():
    result = run_oc_command("oc get projects -o name")
    user_not_logged = result.lower().startswith("error")
    if user_not_logged:
        return jsonify({"current_project": "Not logged in"}), 401
    return jsonify({"projects": result.split()})

@oc_blueprint.route('/change-project', methods=['POST'])
def change_project():
    data = request.json
    result = run_oc_command(f"oc project {data['project']}")
    user_not_logged = result.lower().startswith("error")
    if user_not_logged:
        return jsonify({"current_project": "Not logged in"}), 401
    return jsonify({"current_project": result.strip()})

@oc_blueprint.route('/deployments', methods=['GET'])
def deployment_configs():
    result = run_oc_command("oc get deployments -o name")
    user_not_logged = result.lower().startswith("error")
    if user_not_logged:
        return jsonify({"current_project": "Not logged in"}), 401
    return jsonify({"deployments": result.split()})

@oc_blueprint.route('/restart-deployment/<deployment_name>', methods=['POST'])
def restart_deployment(deployment_name):
    result = run_oc_command(f"oc rollout restart dc/{deployment_name}")
    user_not_logged = result.lower().startswith("error")
    if user_not_logged:
        return jsonify({"current_project": "Not logged in"}), 401
    return jsonify({"result": result.strip()})
