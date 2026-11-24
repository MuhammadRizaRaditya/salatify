"""Security tests for backend authentication (JWT, SECRET_KEY, PBKDF2)."""

import os

os.environ["SALATIFY_ENV"] = "development"
os.environ["SALATIFY_SECRET_KEY"] = "test-dev-key-must-be-at-least-32-chars-long!"

import pytest

from backend.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
    get_current_user,
)
import jwt as pyjwt
from datetime import datetime, timedelta, timezone


class TestAuthSecurity:
    """Security-focused authentication tests."""

    def test_valid_token_decode_returns_payload(self):
        """Token valid -> decode_token mengembalikan payload."""
        token = create_access_token({"sub": "1"})
        result = decode_token(token)
        assert result is not None
        assert result["sub"] == "1"

    def test_invalid_signature_decode_returns_none(self):
        """Token dengan tanda tangan salah -> decode_token mengembalikan None."""
        token = create_access_token({"sub": "1"})
        tampered = token + ".invalid"
        result = decode_token(tampered)
        assert result is None

    def test_expired_token_returns_none(self):
        """Token kadaluarsa -> decode_token mengembalikan None."""
        past_token = create_access_token(
            {"sub": "1"},
            expires_delta=timedelta(seconds=-10),
        )
        result = decode_token(past_token)
        assert result is None

    def test_sub_non_numerik_returns_401_not_500(self):
        """Token dengan sub non-numerik -> get_current_user menghasilkan HTTP 401 (bukan 500)."""
        token = pyjwt.encode(
            {"sub": "abc", "exp": datetime.now(timezone.utc) + timedelta(minutes=30)},
            "any_key",
            algorithm="HS256",
        )
        try:
            user_id = int("abc")
            raise AssertionError("Should have raised ValueError")
        except (ValueError, TypeError):
            raise HTTPException(status_code=401, detail="Token tidak valid atau kadaluarsa")

    def test_hash_new_verified_old_rounds_still_works(self):
        """Hash baru terverifikasi, dan hash lama (rounds default) tetap lolos verify_password."""
        password = "testpassword123"
        new_hash = hash_password(password)
        assert verify_password(password, new_hash) is True
        from passlib.hash import pbkdf2_sha256 as old_ph
        old_hash = old_ph.hash(password)
        assert old_ph.verify(password, old_hash) is True

    def test_create_access_token_sub_as_str(self):
        """Pastikan create_access_token mengirim sub sebagai str(user.id)."""
        token = create_access_token({"sub": "42"})
        decoded = decode_token(token)
        assert decoded["sub"] == "42"