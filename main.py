from displ import Display
import psutil
import time
import datetime

display = Display("/dev/ttyUSB0", 9600, debug=True)

IT = "IT-Cube"
shift = 0 
width = 20 

while True:
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    uptime = time.time() - psutil.boot_time()
    timedata = datetime.datetime.now()

    if shift < len(IT):
        shifted_tr = IT[len(IT)-shift:] + " " * (width - len(IT) + shift)       
    else:         
        shifted_tr = " " * (shift-len(IT)) + IT[:width - (shift-len(IT))]

    display.set_str(f"CPU: {cpu}%     {timedata.strftime('%H:%M')}", 0)
    display.set_str(f"Disk: {disk}%", 1)
    display.set_str(f"Time: {int(uptime / 60)}m {int(uptime % 60)}s", 2)
    display.set_str(f"{shifted_tr}", 3)

    display.update()

    shift = (shift + 1) % (width + len(IT)) 
    time.sleep(1.5)
