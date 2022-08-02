from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import hashlib
backend = default_backend()

def hashInput(input):
    x = str(input)
    x = x.encode('utf-8')
    hash = hashlib.sha256(x)
    hash = hash.hexdigest()
    return hash

def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(message: bytes, token: bytes) -> bytes:
    return Fernet(token).decrypt(message)




