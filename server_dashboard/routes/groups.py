from flask import Blueprint, request, jsonify
import subprocess
import grp 

group_blueprint = Blueprint('groups', __name__)

@group_blueprint.route('/', methods=['GET'])
def get_all_groups():
    all_groups = grp.getgrall()
    group_list = [{'name': group.gr_name, 'GID': group.gr_gid} for group in all_groups]
    return jsonify(groups=group_list, len=len(group_list))

# Route to get a specific group by group name
@group_blueprint.route('/<group_name>', methods=['GET'])
def get_group_by_name(group_name):
    try:
        group_info = grp.getgrnam(group_name)
        group_data = {
            'Group Name': group_info.gr_name,
            'GID': group_info.gr_gid,
            'Members': group_info.gr_mem
        }
        return jsonify(output=group_data)
    except KeyError:
        return jsonify(error=f"Group {group_name} not found"), 404

# Route to get a specific group by group ID
@group_blueprint.route('/gid/<int:group_id>', methods=['GET'])
def get_group_by_id(group_id):
    try:
        group_info = grp.getgrgid(group_id)
        group_data = {
            'name': group_info.gr_name,
            'GID': group_info.gr_gid,
            'Members': group_info.gr_mem
        }
        return jsonify(group_data)
    except KeyError:
        return jsonify(error=f"Group with GID {group_id} not found"), 404
