from flask import Blueprint, request, jsonify
import subprocess
import pwd

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/add', methods=['POST'])
def add_user():
    username = request.json.get('username')
    if not username:
        return jsonify(error="No username provided"), 400
    pwd
    result = subprocess.run(['sudo', 'useradd', username], capture_output=True, text=True)
    return jsonify(output=result.stdout, error=result.stderr)

@users_blueprint.route('/delete/<username>', methods=['DELETE'])
def delete_user(username):
    result = subprocess.run(['sudo', 'userdel', username], capture_output=True, text=True)
    return jsonify(output=result.stdout, error=result.stderr)

@users_blueprint.route('/', methods=['GET'])
def get_all_users():
    users = pwd.getpwall()  
    user_list = [user.pw_name for user in users]
    json = {
        'users': sorted(user_list),
        'len': len(user_list)
    }
    return jsonify(json)

@users_blueprint.route('/<username>', methods=['GET'])
def get_single_user(username):
    user_info = pwd.getpwnam(username)
    user_data = {
        'Username': user_info.pw_name,
        'Password': user_info.pw_passwd,
        'Comment': user_info.pw_gecos,
        'UID': user_info.pw_uid,
        'GID': user_info.pw_gid,
        'Home': user_info.pw_dir,
        'Shell': user_info.pw_shell
    }
    return jsonify(user_data)
