import psutil

def check_port_occupied(port):
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            print(f"Process {conn.pid} is running on port {port}.")

check_port_occupied(3000)
