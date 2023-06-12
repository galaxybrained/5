import socket
import secrets
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.exceptions import InvalidSignature, InvalidKey
from cryptography.hazmat.backends import default_backend
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def generate_session_key():
    return secrets.token_bytes(32)


def generate_salt():
    return secrets.token_bytes(128)


def generate_pbkdf2_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA3_512(),
        length=64,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password)


def derive_key(key, salt):
    hkdf = HKDF(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        info=b'',
        backend=default_backend()
    )
    return hkdf.derive(key)


def encrypt_data(data, session_key):
    iv = get_random_bytes(16)
    cipher = Cipher(algorithms.AES(session_key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return iv + encryptor.tag + ciphertext


def decrypt_data(encrypted_data, session_key):
    iv = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]
    cipher = Cipher(algorithms.AES(session_key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext


def generate_dh_parameters():
    parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
    return parameters


def generate_dh_keypair(parameters):
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key


def serialize_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def deserialize_public_key(serialized_key):
    return serialization.load_pem_public_key(serialized_key, backend=default_backend())


def generate_shared_key(private_key, peer_public_key):
    shared_key = private_key.exchange(peer_public_key)
    return shared_key


def send_file(file_path, host, port):
    password = b'your_password'  # Replace with your own password

    salt = generate_salt()
    derived_key = generate_pbkdf2_key(password, salt)

    parameters = generate_dh_parameters()
    private_key, public_key = generate_dh_keypair(parameters)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))

            serialized_public_key = serialize_public_key(public_key)
            sock.sendall(serialized_public_key)

            received_public_key = sock.recv(4096)
            peer_public_key = deserialize_public_key(received_public_key)

            shared_key = generate_shared_key(private_key, peer_public_key)
            derived_key = derive_key(derived_key, salt)

            encrypted_key = encrypt_data(shared_key, derived_key)
            sock.sendall(encrypted_key)

            with open(file_path, 'rb') as file:
                file_data = file.read()

            encrypted_data = encrypt_data(file_data, shared_key)
            sock.sendall(encrypted_data)

            print("File transfer completed successfully.")
        except (ConnectionRefusedError, ConnectionError) as e:
            print(f"Connection error: {e}")
        except (InvalidSignature, InvalidKey) as e:
            print(f"Encryption error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


def receive_file(save_path, port):
    password = b'your_password'  # Replace with your own password

    salt = generate_salt()
    derived_key = generate_pbkdf2_key(password, salt)

    parameters = generate_dh_parameters()
    private_key, public_key = generate_dh_keypair(parameters)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(('', port))
            sock.listen(1)
            conn, addr = sock.accept()

            received_public_key = conn.recv(4096)
            peer_public_key = deserialize_public_key(received_public_key)

            serialized_public_key = serialize_public_key(public_key)
            conn.sendall(serialized_public_key)

            shared_key = generate_shared_key(private_key, peer_public_key)
            derived_key = derive_key(derived_key, salt)

            received_key = conn.recv(4096)
            decrypted_key = decrypt_data(received_key, derived_key)
            shared_key = decrypt_data(decrypted_key, shared_key)

            received_data = b''
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                received_data += data

            decrypted_data = decrypt_data(received_data, shared_key)

            with open(save_path, 'wb') as file:
                file.write(decrypted_data)

            print("File transfer completed successfully.")
        except (ConnectionRefusedError, ConnectionError) as e:
            print(f"Connection error: {e}")
        except (InvalidSignature, InvalidKey) as e:
            print(f"Decryption error: {e}")
        except InvalidSignature:
            print("Error: Invalid signature. File integrity compromised.")
        except Exception as e:
            print(f"An error occurred: {e}")


def main():
    file_to_send = 'path/to/file.txt'
    received_file = 'path/to/save/received_file.txt'
    host = 'receiver_ip_address'  # IP address of the receiver
    port = 12345  # Choose a suitable port number

    send_file(file_to_send, host, port)
    receive_file(received_file, port)


if __name__ == '__main__':
    main()
