import socket
from cryptography.fernet import Fernet

def generate_key():
    """
    Generates a secure key for encryption/decryption.
    """
    return Fernet.generate_key()

def encrypt_message(key, message):
    """
    Encrypts a message using the provided key.
    """
    cipher_suite = Fernet(key)
    encrypted_message = cipher_suite.encrypt(message.encode())
    return encrypted_message

def decrypt_message(key, encrypted_message):
    """
    Decrypts an encrypted message using the provided key.
    """
    cipher_suite = Fernet(key)
    decrypted_message = cipher_suite.decrypt(encrypted_message)
    return decrypted_message.decode()

# Generate a key
key = generate_key()
print("Generated Key:", key)

# Establish a socket connection
HOST = 'localhost'
PORT = 5000

def start_chat():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print("Chatroom started. Waiting for connection...")

        conn, addr = server_socket.accept()
        print("Connected to:", addr)

        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                encrypted_message = data
                decrypted_message = decrypt_message(key, encrypted_message)
                print("Received:", decrypted_message)

                message = input("Enter your message: ")
                encrypted_message = encrypt_message(key, message)
                conn.sendall(encrypted_message)

start_chat()
