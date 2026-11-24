"""Router autentikasi: registrasi, login, logout, guest, me."""

import os
import re
import secrets
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User
from backend.auth import hash_password, create_access_token, decode_token, get_current_user
from backend.schemas import UserRegister, UserLogin, Token, UserOut

router = APIRouter(prefix="/auth", tags=["Authentication"])

GUEST_USERNAME_PREFIX = "tamu-"
GUEST_EMAIL_SUFFIX = "@guest.salatify.local"
GUEST_USERNAME_BLOCKED = {"tamu", "guest", "admin", "root", "salatify"}
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


@router.post("/register", response_model=UserOut)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    username = payload.username.strip()
    email = payload.email.strip()

    username_lower = username.lower()
    email_lower = email.lower()

    if username_lower.startswith(GUEST_USERNAME_PREFIX) or email_lower.endswith(GUEST_EMAIL_SUFFIX):
        raise HTTPException(
            status_code=400,
            detail="Username dan email tidak dapat dimulai dengan 'tamu-' atau berakhiran '@guest.salatify.local'.",
        )

    blocked_lower = {b.lower(): b for b in GUEST_USERNAME_BLOCKED}
    if username_lower in blocked_lower:
        raise HTTPException(
            status_code=400,
            detail=f"Username '{next(b for b in GUEST_USERNAME_BLOCKED if b.lower() == username_lower)}' adalah username cadangan yang terlindungi.",
        )

    if not re.match(EMAIL_REGEX, email):
        raise HTTPException(status_code=400, detail="Format email tidak valid.")

    if db.query(User).filter(User.username == username_lower).first():
        raise HTTPException(status_code=400, detail="Username sudah digunakan.")
    if db.query(User).filter(User.email == email_lower).first():
        raise HTTPException(status_code=400, detail="Email sudah terdaftar.")

    user = User(
        username=username_lower,
        email=email_lower,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    username = payload.username.strip().lower()
    email = payload.email.strip().lower()

    user = (
        db.query(User)
        .filter((User.username == username) | (User.email == email))
        .first()
    )
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Username/Email atau password salah."
        )
    if user.is_guest:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Username/Email atau password salah."
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Akun tidak aktif.")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/guest", response_model=Token)
def login_guest(db: Session = Depends(get_db), expires_delta: timedelta = timedelta(minutes=int(os.getenv("SALATIFY_GUEST_TOKEN_EXPIRE_MINUTES", "1440")))):
    username = f"tamu-{secrets.token_hex(6)}"
    email = f"{username}@guest.salatify.local"

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(secrets.token_urlsafe(32)),
        is_guest=True,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": str(user.id)}, expires_delta=expires_delta)
    return {"access_token": token, "token_type": "bearer"}
