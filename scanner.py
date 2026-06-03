import socket
import time

target = input("Enter Target IP: ")

start = time.time()

print(f"\nScanning Target: {target}\n")

for port in range(1, 10001):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    result = sock.connect_ex((target, port))

    if result == 0:
        print(f"Port {port} is OPEN")

    sock.close()

end = time.time()

print(f"\nScan Complete!")
print(f"Time Taken: {round(end-start,2)} seconds")
