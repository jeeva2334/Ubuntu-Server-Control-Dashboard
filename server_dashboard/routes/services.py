from flask import Blueprint, jsonify
import subprocess

services_blueprint = Blueprint('services', __name__)

@services_blueprint.route('/', methods=['GET'])
def list_services():
    result = subprocess.run(['systemctl', 'list-units', '--type=service'], capture_output=True, text=True)
    return jsonify(services=result.stdout.splitlines())

@services_blueprint.route('/<action>/<service>', methods=['POST'])
def manage_service(action, service):
    if action in ['start', 'stop', 'restart']:
        result = subprocess.run(['sudo', 'systemctl', action, service], capture_output=True, text=True)
        return jsonify(output=result.stdout, error=result.stderr)
    else:
        return jsonify(error="Invalid action"), 400
