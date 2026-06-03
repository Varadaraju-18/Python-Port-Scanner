import socket
import threading
from queue import Queue
import time
import csv
from datetime import datetime
from colorama import Fore, init
from services import services

init(autoreset=True)

# -----------------------------
# BANNER GRABBER
# -----------------------------

def grab_banner(ip, port):

    try:
        banner_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        banner_socket.settimeout(2)

        banner_socket.connect((ip, port))

        try:
            banner_socket.send(
                b"HEAD / HTTP/1.0\r\n\r\n"
            )
        except:
            pass

        banner = banner_socket.recv(
            1024
        ).decode(
            errors="ignore"
        ).strip()

        banner_socket.close()

        if banner:
            return banner[:100]

        return "No Banner"

    except:
        return "No Banner"


# -----------------------------
# TARGET INPUT
# -----------------------------

target = input(
    "Enter Target IP or Hostname: "
)

try:
    target_ip = socket.gethostbyname(
        target
    )

except socket.gaierror:

    print(
        Fore.RED +
        "[-] Unable to resolve hostname."
    )

    exit()

# -----------------------------
# SCAN MODE
# -----------------------------

print("\nSelect Scan Mode")
print("1. Quick Scan")
print("2. Standard Scan")
print("3. Full Scan")

choice = input(
    "\nEnter Choice (1-3): "
)

if choice == "1":

    ports_to_scan = [
        20, 21, 22, 23, 25,
        53, 80, 110, 143,
        443, 445, 993, 995,
        3306, 3389, 5432,
        5900, 6379, 8080,
        8443, 9000, 9929
    ]

    mode = "Quick Scan"

elif choice == "2":

    ports_to_scan = range(
        1,
        10001
    )

    mode = "Standard Scan"

elif choice == "3":

    ports_to_scan = range(
        1,
        65536
    )

    mode = "Full Scan"

else:

    print(
        Fore.RED +
        "Invalid Choice"
    )

    exit()

print(
    Fore.CYAN +
    f"\nScanning Target: {target} ({target_ip})"
)

print(
    Fore.CYAN +
    f"Mode: {mode}\n"
)

# -----------------------------
# INITIALIZATION
# -----------------------------

start_time = time.time()

queue = Queue()

open_ports = []

timestamp = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)

# -----------------------------
# PORT SCANNER
# -----------------------------

def scan_port():

    while not queue.empty():

        port = queue.get()

        try:

            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            sock.settimeout(1)

            result = sock.connect_ex(
                (target_ip, port)
            )

            if result == 0:

                service = services.get(
                    port,
                    "Unknown Service"
                )

                banner = grab_banner(
                    target_ip,
                    port
                )

                print(
                    Fore.GREEN +
                    f"[OPEN] Port {port} ({service})"
                )

                if banner != "No Banner":

                    print(
                        Fore.YELLOW +
                        f"Banner: {banner}"
                    )

                open_ports.append(
                    (
                        port,
                        service,
                        banner
                    )
                )

            sock.close()

        except:
            pass

        queue.task_done()

# -----------------------------
# ADD PORTS
# -----------------------------

for port in ports_to_scan:

    queue.put(port)

# -----------------------------
# THREADS
# -----------------------------

for _ in range(100):

    thread = threading.Thread(
        target=scan_port
    )

    thread.daemon = True

    thread.start()

queue.join()

# -----------------------------
# RESULTS
# -----------------------------

end_time = time.time()

print(
    Fore.CYAN +
    "\n========== RESULTS ==========\n"
)

if open_ports:

    for port, service, banner in sorted(
        open_ports
    ):

        print(
            Fore.GREEN +
            f"Port {port} OPEN ({service})"
        )

        if banner != "No Banner":

            print(
                Fore.YELLOW +
                f"Banner: {banner}"
            )

else:

    print(
        Fore.YELLOW +
        "No open ports found."
    )

print(
    Fore.MAGENTA +
    f"\nTotal Open Ports: {len(open_ports)}"
)

print(
    Fore.MAGENTA +
    f"Scan Time: {round(end_time-start_time,2)} seconds"
)

# -----------------------------
# TXT REPORT
# -----------------------------

with open(
    "reports/scan_results.txt",
    "w"
) as file:

    file.write(
        "PORT SCAN REPORT\n"
    )

    file.write(
        "=" * 50 + "\n"
    )

    file.write(
        f"Target: {target}\n"
    )

    file.write(
        f"Resolved IP: {target_ip}\n"
    )

    file.write(
        f"Scan Mode: {mode}\n"
    )

    file.write(
        f"Date: {timestamp}\n\n"
    )

    for port, service, banner in sorted(
        open_ports
    ):

        file.write(
            f"Port {port} OPEN ({service})\n"
        )

        file.write(
            f"Banner: {banner}\n\n"
        )

    file.write(
        f"Total Open Ports: {len(open_ports)}\n"
    )

    file.write(
        f"Scan Time: {round(end_time-start_time,2)} seconds\n"
    )

# -----------------------------
# CSV REPORT
# -----------------------------

with open(
    "reports/scan_results.csv",
    "w",
    newline=""
) as csvfile:

    writer = csv.writer(
        csvfile
    )

    writer.writerow(
        [
            "Port",
            "Service",
            "Banner"
        ]
    )

    for port, service, banner in sorted(
        open_ports
    ):

        writer.writerow(
            [
                port,
                service,
                banner
            ]
        )

print(
    Fore.CYAN +
    "\nReports saved successfully!"
)

print(
    Fore.GREEN +
    "TXT -> reports/scan_results.txt"
)

print(
    Fore.GREEN +
    "CSV -> reports/scan_results.csv"
)