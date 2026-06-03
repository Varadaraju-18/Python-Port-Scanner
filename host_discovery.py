import socket
import threading
from queue import Queue

network = input(
    "Enter Network (Example: 192.168.1): "
)

queue = Queue()

live_hosts = []


def discover_host():

    while not queue.empty():

        ip = queue.get()

        try:

            ports = [22, 80, 443]

            host_found = False

            for port in ports:

                sock = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM
                )

                sock.settimeout(0.2)

                result = sock.connect_ex(
                    (ip, port)
                )

                sock.close()

                if result == 0:

                    host_found = True

                    break

            if host_found:

                print(f"[LIVE] {ip}")

                live_hosts.append(ip)

        except:
            pass

        queue.task_done()


for i in range(1, 255):

    ip = f"{network}.{i}"

    queue.put(ip)


for _ in range(100):

    thread = threading.Thread(
        target=discover_host
    )

    thread.daemon = True

    thread.start()


queue.join()

print(
    "\n========== LIVE HOSTS ==========\n"
)

if live_hosts:

    for host in live_hosts:

        print(host)

else:

    print(
        "No live hosts found."
    )