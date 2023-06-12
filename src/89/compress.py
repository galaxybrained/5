import os
import shutil
import zipfile
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import getpass
import sys
import cryptography


def derive_key(password, salt):
    backend = default_backend()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA3_512(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    return kdf.derive(password)


def compress_file():
    file_path = input("Enter the file path: ")
    if not os.path.isfile(file_path):
        print("Invalid file path.")
        return

    password = getpass.getpass("Enter the password for the ZIP file (hidden): ")
    salt = os.urandom(16)
    key = derive_key(password.encode(), salt)

    base_name = os.path.basename(file_path)
    zip_path = os.path.splitext(file_path)[0] + '.zip'

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr('salt', salt)
        zipf.writestr('iv', os.urandom(12))

        with open(file_path, 'rb') as file:
            data = file.read()

        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(os.urandom(16), data, None)

        zipf.writestr(base_name, ciphertext)

    print(f'File compressed successfully: {zip_path}')
    os.remove(file_path)
    sys.exit(0)


def compress_directory():
    directory_path = input("Enter the directory path: ")
    if not os.path.isdir(directory_path):
        print("Invalid directory path.")
        return

    password = getpass.getpass("Enter the password for the ZIP file (hidden): ")
    salt = os.urandom(16)
    key = derive_key(password.encode(), salt)

    base_name = os.path.basename(directory_path)
    zip_path = directory_path + '.zip'

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr('salt', salt)
        zipf.writestr('iv', os.urandom(12))

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)

                with open(file_path, 'rb') as file:
                    data = file.read()

                aesgcm = AESGCM(key)
                ciphertext = aesgcm.encrypt(os.urandom(16), data, None)

                zipf.writestr(os.path.relpath(file_path, directory_path), ciphertext)

    print(f'Directory compressed successfully: {zip_path}')
    shutil.rmtree(directory_path)
    sys.exit(0)


def extract_zip():
    zip_path = input("Enter the ZIP file path: ")
    if not os.path.isfile(zip_path):
        print("Invalid ZIP file path.")
        return

    password = getpass.getpass("Enter the password for the ZIP file (hidden): ")

    with zipfile.ZipFile(zip_path, 'r') as zipf:
        try:
            salt = zipf.read('salt')
            iv = zipf.read('iv')

            password_key = derive_key(password.encode(), salt)
            aesgcm = AESGCM(password_key)

            for file_info in zipf.infolist():
                if file_info.filename == 'salt' or file_info.filename == 'iv':
                    continue

                encrypted_data = zipf.read(file_info.filename)
                plaintext = aesgcm.decrypt(iv, encrypted_data, None)
                with open(file_info.filename, 'wb') as file:
                    file.write(plaintext)

            print(f'ZIP file extracted successfully.')
            os.remove(zip_path)
            sys.exit(0)
        except (ValueError, cryptography.exceptions.InvalidTag):
            print("Incorrect password.")
            sys.exit(1)


while True:
    print("\n1. Compress file\n2. Compress directory\n3. Extract ZIP file\n4. Quit")
    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        compress_file()
    elif choice == "2":
        compress_directory()
    elif choice == "3":
        extract_zip()
    elif choice == "4":
        sys.exit(0)
    else:
        print("Invalid choice. Please try again.")
