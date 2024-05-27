from cryptography.fernet import Fernet
import binascii
import os
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def derive_key(password, iterations=100000, key_length=32):
    """
    Derive a cryptographic key from a password using PBKDF2.

    Args:
        password (bytes): The password as bytes.
        salt (bytes): The salt value as bytes.
        iterations (int): The number of iterations for PBKDF2 (default: 100000).
        key_length (int): The length of the derived key in bytes (default: 32).

    Returns:
        bytes: The derived key.
    """
    salt = b'\x98\x8e\x92~\x87\x0b\x812;/2\xf4\xa6^\xd7\x03' 
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=key_length,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    key = kdf.derive(binascii.unhexlify(password))
    return base64.urlsafe_b64encode(key)

def encrypt_password(password, encryption_key):
    cipher = Fernet(encryption_key)
    return cipher.encrypt(password.encode())

def decrypt_password(encrypted_password, encryption_key):
    cipher = Fernet(encryption_key)
    return cipher.decrypt(encrypted_password).decode()


