import socket
from cryptography.fernet import Fernet

def start_client():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 5555))
        
        # Receive the encryption key from the server
        key = client.recv(1024)
        cipher_suite = Fernet(key)
        
        print("Connected to the server. Type your message (type 'exit' to quit):")
        
        while True:
            # Get user input
            message = input("> ")
            if message.lower() == 'exit':
                break
            
            # Encrypt and send the message
            encrypted_message = cipher_suite.encrypt(message.encode())
            client.send(encrypted_message)
            
            # Receive and decrypt the server's response
            encrypted_response = client.recv(1024)
            response = cipher_suite.decrypt(encrypted_response).decode()
            print(f"Response from server: {response}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()
        print("Connection closed.")

if __name__ == "__main__":
    start_client()