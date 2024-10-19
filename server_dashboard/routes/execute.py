from flask import Blueprint, request, jsonify
import subprocess

execute_blueprint = Blueprint('execute', __name__)

@execute_blueprint.route('/', methods=['POST'])
def execute_command():
    command = request.json.get('command')
    if not command:
        return jsonify(error="No command provided"), 400

    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return jsonify(output=result.stdout, error=result.stderr)
