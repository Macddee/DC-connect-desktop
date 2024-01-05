import threading
import subprocess
import socket
import time
def thrd():
    host="8.8.8.8"
    port=53
    timeout=3
    while True:
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            
            # lblWifi = ctk.CTkLabel(master=leftMenu, image=svg.SvgImage(file="images/wifi.svg"), text="fsd")
            print("there is net")            
        except OSError as ex:
            print("no net")
            # print(ex)
            
            
        time.sleep(3)


internet_thread = threading.Thread(target=thrd)
internet_thread.daemon = True
internet_thread.start()

while True:
    print("halo threading world!")
    time.sleep(3)