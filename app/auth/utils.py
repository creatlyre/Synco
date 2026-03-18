import base64
import hashlib

from cryptography.fernet import Fernet

from config import Settings


def _get_cipher() -> Fernet:
    settings = Settings()
    key_material = settings.DB_ENCRYPTION_KEY.encode("utf-8")
    digest = hashlib.sha256(key_material).digest()
    fernet_key = base64.urlsafe_b64encode(digest)
    return Fernet(fernet_key)


def encrypt_token(token: str) -> str:
    cipher = _get_cipher()
    return cipher.encrypt(token.encode("utf-8")).decode("utf-8")


def decrypt_token(encrypted_token: str) -> str:
    cipher = _get_cipher()
    return cipher.decrypt(encrypted_token.encode("utf-8")).decode("utf-8")
