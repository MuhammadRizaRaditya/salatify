"""Validator input aplikasi."""

import re


EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email: str) -> bool:
    if not email:
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def is_valid_password(password: str) -> tuple:
    """Mengembalikan (is_valid, message)."""
    if not password:
        return False, "Password tidak boleh kosong."
    if len(password) < 6:
        return False, "Password minimal 6 karakter."
    return True, ""


def validate_required(value, field_name: str) -> tuple:
    if value is None or str(value).strip() == "":
        return False, f"{field_name} tidak boleh kosong."
    return True, ""
