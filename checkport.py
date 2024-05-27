# this file was used in the early stages when choosing the port for 
# the REDIRECT_URI from the Spotify API. Port 3000 is not working on my machine 
# as i already have another backgorund process at this port, therefore i chose
# a different one.

import psutil

def check_port_occupied(port):
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            print(f"Process {conn.pid} is running on port {port}.")

check_port_occupied(3000)
