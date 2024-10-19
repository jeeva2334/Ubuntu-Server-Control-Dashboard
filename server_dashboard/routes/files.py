from flask import Blueprint, request, jsonify, send_from_directory
import os

files_blueprint = Blueprint('files', __name__)

UPLOAD_FOLDER = '/path/to/upload/folder'

@files_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify(message="File uploaded successfully")

@files_blueprint.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        return jsonify(error="File not found"), 404
