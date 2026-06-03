import socket
import threading
from queue import Queue

from services import services


# ---------------------------------
# BANNER GRABBER
# ---------------------------------

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


# ---------------------------------
# MAIN SCANNER
# ---------------------------------

def scan_target(target, mode):

    results = []

    try:

        target_ip = socket.gethostbyname(
            target
        )

    except socket.gaierror:

        return [
            "Unable to resolve hostname."
        ]

    results.append(
        f"Target: {target}"
    )

    results.append(
        f"Resolved IP: {target_ip}"
    )

    results.append(
        f"Scan Mode: {mode}"
    )

    results.append(
        "-" * 40
    )

    # -----------------------------
    # SCAN MODES
    # -----------------------------

    if mode == "Quick":

        ports_to_scan = [
            20, 21, 22, 23, 25,
            53, 80, 110, 143,
            443, 445, 993, 995,
            1716, 3306, 3389,
            5432, 5900, 6379,
            8080, 8443, 9000,
            9929
        ]

    elif mode == "Standard":

        ports_to_scan = range(
            1,
            10001
        )

    elif mode == "Full":

        ports_to_scan = range(
            1,
            65536
        )

    else:

        return [
            "Invalid scan mode selected."
        ]

    # -----------------------------
    # THREADING
    # -----------------------------

    queue = Queue()

    open_ports = []

    lock = threading.Lock()

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

                sock.settimeout(0.5)

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

                    with lock:

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
    # START THREADS
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

    if open_ports:

        for port, service, banner in sorted(
            open_ports
        ):

            results.append(
                f"[OPEN] Port {port} ({service})"
            )

            if banner != "No Banner":

                results.append(
                    f"Banner: {banner}"
                )

            results.append("")

        results.append(
            "-" * 40
        )

        results.append(
            f"Total Open Ports: {len(open_ports)}"
        )

    else:

        results.append(
            "No open ports found."
        )

    return results