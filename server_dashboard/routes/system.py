from flask import Blueprint, jsonify
import psutil
import time
from linux_metrics import cpu_stat

system_blueprint = Blueprint('system', __name__)

def get_cpu_uptime():
    boot_time = psutil.boot_time()  # Get the boot time in seconds since epoch
    current_time = time.time()  # Get the current time in seconds since epoch
    uptime_seconds = current_time - boot_time  # Calculate uptime in seconds

    # Calculate hours, minutes, and seconds
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Return uptime in hours, minutes, and seconds
    return int(hours), int(minutes), int(seconds)  # Return uptime in seconds, minutes, hours

@system_blueprint.route('/', methods=['GET'])
def get_system_metrics():
    # Get CPU utilization quickly
    cpu_pcts = cpu_stat.cpu_percents(1)  # Reduced from 5 to 1 second for faster polling
    cpu_utilization = 100 - cpu_pcts['idle']
    cpu_tasks = cpu_stat.procs_running()

    # Get memory stats
    memory = psutil.virtual_memory()
    memory_usage_percentage = memory.percent
    memory_used_gb = round(memory.used / (1024 ** 3), 2)
    memory_total_gb = round(memory.total / (1024 ** 3), 2)

    # Get uptime
    uptime = get_cpu_uptime()

    return jsonify({
        'cpu_utilization': cpu_utilization,
        'cpu_tasks': cpu_tasks,
        'memory_usage_percentage': memory_usage_percentage,
        'memory_used_gb': memory_used_gb,
        'memory_total_gb': memory_total_gb,
        'uptime_seconds': uptime[2],
        'uptime_minutes': uptime[1],
        'uptime_hours': uptime[0]
    })