from linux_metrics import cpu_stat, disk_usage, mem_stats
import psutil
import time

def get_cpu_uptime():
    boot_time = psutil.boot_time()  # Get the boot time in seconds since epoch
    current_time = time.time()  # Get the current time in seconds since epoch
    uptime_seconds = current_time - boot_time  # Calculate uptime in seconds
    uptime_minutes = uptime_seconds / 60  # Convert to minutes
    uptime_hours = uptime_minutes / 60  # Convert to hours
    return uptime_seconds, uptime_minutes, uptime_hours

while True:
    cpu_pcts = cpu_stat.cpu_percents(5)
    print(f'CPU utilization: {100 - cpu_pcts["idle"]:.2f}%')
    print(f'CPU Tasks: {cpu_stat.procs_running()}')
    # print(f'Disk Usage: {disk_usage()}')
    memory = psutil.virtual_memory()
    memory_usage_percentage = memory.percent
    print(f'MEM Status: {memory_usage_percentage}% Total Usage:{round(memory.used / (1024 ** 3), 2)} / {round(memory.total / (1024 ** 3), 2)}')
    print(f'UpTime: {get_cpu_uptime()}')