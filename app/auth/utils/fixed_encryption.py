import base64
import hashlib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class FixedEncryption:
    def __init__(self, key: bytes):
        self._key = base64.urlsafe_b64decode(key)
        if len(self._key) != 32:
            raise ValueError("Key must be 32 url-safe base64-encoded bytes.")

    def encrypt(self, data: bytes) -> bytes:
        iv = hashlib.sha256(data).digest()[:16]

        cipher = Cipher(algorithms.AES(self._key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        block_size = 16
        padding_length = block_size - (len(data) % block_size)
        padded_data = data + bytes([padding_length]) * padding_length

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return base64.urlsafe_b64encode(iv + ciphertext)

    def decrypt(self, encrypted_data: bytes) -> bytes:
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data)
        except Exception:
            encrypted_bytes = encrypted_data

        iv = encrypted_bytes[:16]

        ciphertext = encrypted_bytes[16:]

        cipher = Cipher(algorithms.AES(self._key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        padding_length = padded_plaintext[-1]
        if padding_length < 1 or padding_length > 16:
            raise ValueError("Invalid padding")

        if padded_plaintext[-padding_length:] != bytes([padding_length]) * padding_length:
            raise ValueError("Invalid padding")

        return padded_plaintext[:-padding_length]