import random
import string
import hashlib
import hmac

def generate_password(length=12, include_digits=True, include_symbols=True):
    characters = string.ascii_letters
    if include_digits:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def hash_password_sha3_hmac(password, secret_key):
    sha3_512 = hashlib.sha3_512()
    sha3_512.update(password.encode('utf-8'))
    hmac_obj = hmac.new(secret_key.encode('utf-8'), sha3_512.digest(), hashlib.sha3_512)
    hashed_password = hmac_obj.hexdigest()
    return hashed_password

if __name__ == "__main__":
    password = generate_password()
    secret_key = generate_password()

    hashed_password_sha3_hmac = hash_password_sha3_hmac(password, secret_key)

    print("Generated password:", password)
    print("Generated secret key:", secret_key)
    print("Hashed password (SHA-3-512 HMAC):", hashed_password_sha3_hmac)
