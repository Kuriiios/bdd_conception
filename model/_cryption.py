
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f= Fernet(key)

def encrypt(data):
    return f.encrypt(data.encode('utf-8'))

def decrypt(data):
    return f.decrypt(data.decode('utf-8'))