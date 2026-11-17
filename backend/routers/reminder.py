"""Router pengingat sholat (preferensi) - alias untuk frontend."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import PrayerPreferences, User
from backend.auth import get_current_user
from backend.schemas import PrayerPreferencesIn, PrayerPreferencesOut

router = APIRouter(prefix="/reminder", tags=["Pengingat Sholat"])


@router.get("", response_model=PrayerPreferencesOut)
def get_reminder(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    pref = db.query(PrayerPreferences).filter(PrayerPreferences.user_id == current_user.id).first()
    if not pref:
        pref = PrayerPreferences(user_id=current_user.id)
        db.add(pref)
        db.commit()
        db.refresh(pref)
    return pref


@router.put("", response_model=PrayerPreferencesOut)
def set_reminder(
    payload: PrayerPreferencesIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pref = db.query(PrayerPreferences).filter(PrayerPreferences.user_id == current_user.id).first()
    if not pref:
        pref = PrayerPreferences(user_id=current_user.id)
        db.add(pref)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(pref, field, value)
    db.commit()
    db.refresh(pref)
    return pref
