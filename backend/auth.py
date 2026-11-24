"""Utilitas autentikasi JWT, hashing password, dan dependensi user saat ini."""

import os
import secrets
import warnings
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.hash import pbkdf2_sha256
import jwt

from backend.database import get_db
from backend.models import User

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("SALATIFY_TOKEN_EXPIRE_MINUTES", "10080"))  # 7 hari

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def _get_secret_key():
    """Ambil SECRET_KEY dari env, dengan validasi dan fallback development."""
    env = os.getenv("SALATIFY_ENV", "production")
    secret_key = os.getenv("SALATIFY_SECRET_KEY")
    if secret_key is None or len(secret_key) < 32:
        if env == "development":
            secret_key = secrets.token_urlsafe(48)
            warnings.warn(
                "SALATIFY_SECRET_KEY tidak diatur; dibuat key sementara untuk development. "
                "Token akan tidak valid setelah restart dengan key yang benar.",
                stacklevel=2,
            )
        else:
            raise RuntimeError(
                "SALATIFY_SECRET_KEY wajib diatur di environment produksi. "
                "Gunakan: python -c \"import secrets; print(secrets.token_urlsafe(48))\""
            )
    return secret_key


SECRET_KEY = _get_secret_key()


def hash_password(password: str) -> str:
    return pbkdf2_sha256.using(rounds=600_000).hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pbkdf2_sha256.verify(plain_password, hashed_password)
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"require": ["exp", "sub"]},
        )
    except jwt.PyJWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token tidak valid atau kadaluarsa")
    try:
        user_id = int(payload.get("sub", ""))
    except (ValueError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token tidak valid atau kadaluarsa")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Pengguna tidak ditemukan")
    return user