import random
import string

validchars = 'abcdefghijklmnopqrstuvwxyz1234567890'
domains = ["@gmail.com", "@hotmail.com", "@yahoo.com", "@protonmail.com"]

def generate_random_login():
    login = ''
    loginlen = random.randint(4, 15)
    for _ in range(loginlen):
        pos = random.randint(0, len(validchars) - 1)
        login += validchars[pos]
    if login[0].isnumeric():
        pos = random.randint(0, len(validchars) - 10)
        login = validchars[pos] + login
    return login

def generate_random_password():
    password = ''
    passwordlen = 20
    valid_chars = string.ascii_letters + string.digits + string.punctuation
    for _ in range(passwordlen):
        pos = random.randint(0, len(valid_chars) - 1)
        password += valid_chars[pos]
    return password

def generate_and_check_email():
    login = generate_random_login()
    domain = random.choice(domains)
    email = login + domain
    password = generate_random_password()
    print("Email:", email)
    print("Password:", password)

generate_and_check_email()
