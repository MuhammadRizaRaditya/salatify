"""Router profil dan pengaturan pengguna."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User, UserSettings
from backend.auth import get_current_user, hash_password, verify_password
from backend.schemas import UserOut, UserSettingsIn, UserSettingsOut, PasswordChange

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/password")
def change_password(
    payload: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.is_guest:
        raise HTTPException(status_code=400, detail="Tidak tersedia untuk pengguna tamu.")
    if not verify_password(payload.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Password lama salah.")
    if len(payload.new_password) < 6:
        raise HTTPException(status_code=400, detail="Password minimal 6 karakter.")
    current_user.password_hash = hash_password(payload.new_password)
    db.commit()
    return {"message": "Password berhasil diubah."}


@router.get("/settings", response_model=UserSettingsOut)
def get_settings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.id).first()
    if not settings:
        settings = UserSettings(user_id=current_user.id)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


@router.put("/settings", response_model=UserSettingsOut)
def update_settings(
    payload: UserSettingsIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.id).first()
    if not settings:
        settings = UserSettings(user_id=current_user.id)
        db.add(settings)
    settings.tema_gelap = payload.tema_gelap if payload.tema_gelap is not None else settings.tema_gelap
    settings.nama_lengkap = payload.nama_lengkap if payload.nama_lengkap is not None else settings.nama_lengkap
    settings.email = payload.email if payload.email is not None else settings.email
    db.commit()
    db.refresh(settings)
    return settings
