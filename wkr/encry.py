import os
import importlib.util
import subprocess
import platform

def clear_screen():
    # Clear screen based on the OS
    if platform.system() == 'Windows':
        os.system('cls')
    elif platform.system() == 'Linux' and 'TERMUX' in os.environ: os.system('clear')

    else:
        os.system('clear')
# Check if pycryptodome is installed, if not, install it
if importlib.util.find_spec("Crypto") is None:
    print("Installing pycryptodome...")
    subprocess.check_call(["pip", "install", "pycryptodome"])
    clear_screen()
# Check if getpass module is available
if importlib.util.find_spec("getpass") is None:
    print("Error: 'getpass' module is not available.")
    exit(1)
# Import required modules
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import getpass

def encrypt_file(key, file_path):
    cipher = AES.new(key, AES.MODE_GCM)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    ciphertext, tag = cipher.encrypt_and_digest(pad(file_data, AES.block_size))
    encrypted_file_path = file_path + '.encrypted'
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(cipher.nonce + tag + ciphertext)
    os.remove(file_path)  # Delete the original file

def decrypt_file(key, encrypted_file_path):
    with open(encrypted_file_path, 'rb') as encrypted_file:
        nonce = encrypted_file.read(16)
        tag = encrypted_file.read(16)
        ciphertext = encrypted_file.read()
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    decrypted_data = unpad(cipher.decrypt_and_verify(ciphertext, tag), AES.block_size)
    
    decrypted_file_path = os.path.splitext(encrypted_file_path)[0]  # Remove '.encrypted' extension
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)
    os.remove(encrypted_file_path)  # Delete the encrypted file

def derive_key(passphrase, salt):
    from Crypto.Protocol.KDF import PBKDF2
    return PBKDF2(passphrase, salt, dkLen=32, count=100000)

def encrypt_key(key, passphrase):
    salt = get_random_bytes(16)
    derived_key = derive_key(passphrase, salt)
    cipher = AES.new(derived_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(key)
    return salt + cipher.nonce + tag + ciphertext

def decrypt_key(encrypted_key, passphrase):
    salt = encrypted_key[:16]
    nonce = encrypted_key[16:32]
    tag = encrypted_key[32:48]
    ciphertext = encrypted_key[48:]
    derived_key = derive_key(passphrase, salt)
    cipher = AES.new(derived_key, AES.MODE_GCM, nonce)
    key = cipher.decrypt_and_verify(ciphertext, tag)
    return key

def store_key(key, passphrase, key_file):
    encrypted_key = encrypt_key(key, passphrase)
    with open(key_file, 'wb') as file:
        file.write(encrypted_key)

def retrieve_key(passphrase, key_file):
    with open(key_file, 'rb') as file:
        encrypted_key = file.read()
    key = decrypt_key(encrypted_key, passphrase)
    return key

def delete_key_file(key_file):
    try:
        os.remove(key_file)
    except OSError:
        pass

def main():
    choice = input("Enter 'e' to encrypt or 'd' to decrypt: ")

    if choice == 'e':
        key = get_random_bytes(32)  # Generate a random 256-bit key
        file_path = input("Enter the path of the file to encrypt: ")
        encrypt_file(key, file_path)
        passphrase = getpass.getpass("Enter a passphrase to encrypt the encryption key: ")
        key_file = input("Enter the path to store the encrypted key: ")
        store_key(key, passphrase, key_file)
        print("File encrypted successfully.")
    elif choice == 'd':
        passphrase = getpass.getpass("Enter the passphrase to decrypt the encryption key: ")
        key_file = input("Enter the path to retrieve the encrypted key: ")
        key = retrieve_key(passphrase, key_file)
        encrypted_file_path = input("Enter the path of the encrypted file: ")
        decrypt_file(key, encrypted_file_path)
        delete_key_file(key_file)
        print("File decrypted successfully. The key file has been deleted.")
    else:
        print("Invalid choice.")

if __name__ == '__main__':
    main()
