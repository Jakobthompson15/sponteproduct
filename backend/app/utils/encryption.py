"""
Encryption utilities for securing sensitive data like OAuth tokens.
Uses Fernet symmetric encryption from cryptography library.
"""

from cryptography.fernet import Fernet
from app.config import settings
import base64
import hashlib


def get_fernet_key() -> bytes:
    """
    Generate a Fernet key from the SECRET_KEY.
    Fernet requires exactly 32 url-safe base64-encoded bytes.
    """
    # Hash the SECRET_KEY to get consistent 32 bytes
    key_bytes = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return base64.urlsafe_b64encode(key_bytes)


def encrypt_token(token: str) -> str:
    """
    Encrypt a token (like OAuth access_token or refresh_token).

    Args:
        token: Plain text token to encrypt

    Returns:
        Encrypted token as string
    """
    fernet = Fernet(get_fernet_key())
    encrypted = fernet.encrypt(token.encode())
    return encrypted.decode()


def decrypt_token(encrypted_token: str) -> str:
    """
    Decrypt an encrypted token.

    Args:
        encrypted_token: Encrypted token string

    Returns:
        Decrypted plain text token
    """
    fernet = Fernet(get_fernet_key())
    decrypted = fernet.decrypt(encrypted_token.encode())
    return decrypted.decode()
