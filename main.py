import psutil
import time
import datetime
from displ import Display, get_port_list
import gpustat


def get_cpu_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            for entry in temps['coretemp']:
                if entry.label.startswith('Core'):
                    return entry.current
        return None
    except Exception as e:
        print(f"Error getting CPU temperature: {e}")
        return None


def get_system_uptime():
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_days = int(uptime_seconds // (24 * 3600))
    uptime_hours = int((uptime_seconds % (24 * 3600)) // 3600)
    uptime_minutes = int((uptime_seconds % 3600) // 60)
    return f"{uptime_days}d {uptime_hours}h {uptime_minutes}m"

def get_ram_usage():
    return psutil.virtual_memory().percent

def get_disk_usage():
    return psutil.disk_usage('/').percent

def get_network_stats():
    net_io = psutil.net_io_counters()
    sent_kb = net_io.bytes_sent // 1024
    recv_kb = net_io.bytes_recv // 1024
    return f"Tx:{sent_kb}KB Rx:{recv_kb}KB"

def get_most_resource_intensive_process():
    processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), key=lambda proc: proc.info['cpu_percent'], reverse=True)
    if processes:
        top_process = processes[0]
        return f"{top_process.info['name'][:8]}" #truncate
    else:
        return "None"


def display_info(display):
    while True:
        now = datetime.datetime.now().strftime("%H:%M")

        temp = get_cpu_temperature()
        gpu_stats = gpustat.GPUStatCollection.new_query()
        gpu_temp = None
        for gpu in gpu_stats.gpus:
            gpu_temp = gpu.temperature
            gpu_utilization = gpu.utilization
            break

        cpu_str = f"CPU: {temp:.0f}C" if temp is not None else f"CPU: {psutil.cpu_percent()}%"
        gpu_str = f"GPU: {gpu_temp:.0f}C" if gpu_temp is not None else "GPU:N/A"

        display.set_str(f"{cpu_str}", line=3)
        display.set_str(f"{gpu_str}       {now}", line=0)


        display.set_str(f"RAM: {get_ram_usage()}%", line=2)


        display.set_str(f"GPU: {gpu_utilization}%", line=1)


        display.update()
        time.sleep(2)


if __name__ == '__main__':
    ports = get_port_list()

    if ports:
        port = ports[1]
        print(f"Using port: {port}")
    else:
        print("No available COM ports found. Make sure the display is connected.")
        exit()

    display = Display(port=port, boudrate=9600, debug=True)

    if display.echo():
        print("Echo test passed!")
    else:
        print("Echo test failed.")

    display_info(display)