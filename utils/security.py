"""Utilitas keamanan: hashing password dan verifikasi."""

from passlib.hash import pbkdf2_sha256


def hash_password(password: str) -> str:
    """Hash password dengan PBKDF2-SHA256 (tidak disimpan sebagai teks biasa)."""
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verifikasi password terhadap hash yang tersimpan."""
    try:
        return pbkdf2_sha256.verify(password, hashed)
    except Exception:
        return False
