from flask import Blueprint, jsonify
import subprocess

services_blueprint = Blueprint('services', __name__)

@services_blueprint.route('/', methods=['GET'])
def list_services():
    result = subprocess.run(['systemctl', 'list-units', '--type=service', '--all'], capture_output=True, text=True)

    # Split the output into lines and extract relevant details
    services = []
    for line in result.stdout.splitlines()[1:]:  # Skip the header line
        if line.strip():  # Ignore empty lines
            parts = line.split()  # Split by whitespace
            if len(parts) >= 5:  # Ensure there are enough parts
                service_info = {
                    'name': parts[0],  # Service name
                    'loaded': parts[1],  # Loaded status
                    'active': parts[2],  # Active status
                    'sub': parts[3] if len(parts) > 3 else '',
                    'desc': parts[4] if len(parts) > 3 else ''
                }
                services.append(service_info)

    return jsonify(services)


@services_blueprint.route('/<action>/<service>', methods=['POST'])
def manage_service(action, service):
    if action in ['start', 'stop', 'restart']:
        result = subprocess.run(['sudo', 'systemctl', action, service], capture_output=True, text=True)
        return jsonify(output=result.stdout, error=result.stderr)
    else:
        return jsonify(error="Invalid action"), 400
