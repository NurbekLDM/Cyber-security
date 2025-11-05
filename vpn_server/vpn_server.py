import socket
import threading
from cryptography.fernet import Fernet

# Generate a key and cipher suite
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def handle_client(client_socket, address):
    print(f"Connection from {address} has been established.")
    
    # Send the encryption key to the client (insecure, replace with a secure key exchange in production)
    client_socket.send(key)
    
    while True:
        try:
            # Receive encrypted data from the client
            encrypted_data = client_socket.recv(1024)
            if not encrypted_data:
                break
            
            # Decrypt the data
            data = cipher_suite.decrypt(encrypted_data).decode()
            print(f"Received from {address}: {data}")
            
            # Prepare and send an encrypted response
            response = f"Server received: {data}"
            encrypted_response = cipher_suite.encrypt(response.encode())
            client_socket.send(encrypted_response)
        except Exception as e:
            print(f"Error: {e}")
            break
    
    client_socket.close()
    print(f"Connection from {address} has been closed.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5555))
    server.listen(5)
    print("Server is listening...")
    
    while True:
        client_socket, address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    start_server()