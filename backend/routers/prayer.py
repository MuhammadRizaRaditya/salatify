"""Router jadwal sholat dan preferensi."""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import JadwalSholat, PrayerPreferences, User
from backend.auth import get_current_user
from backend.schemas import PrayerTimeOut, PrayerPreferencesIn, PrayerPreferencesOut
from backend.services.prayer_service import PrayerService

router = APIRouter(prefix="/prayer", tags=["Jadwal Sholat"])
service = PrayerService()


def _to_out(row: JadwalSholat) -> PrayerTimeOut:
    return PrayerTimeOut(
        tanggal=row.tanggal,
        subuh=row.subuh, dzuhur=row.dzuhur, ashar=row.ashar,
        maghrib=row.maghrib, isya=row.isya,
        lokasi=row.lokasi, latitude=row.latitude, longitude=row.longitude,
        metode=row.metode,
    )


@router.get("/jadwal", response_model=PrayerTimeOut)
def jadwal_hari_ini(
    latitude: str = Query("-6.2"),
    longitude: str = Query("106.8"),
    metode: str = Query("mwml"),
    tanggal: str | None = Query(None),
    db: Session = Depends(get_db),
):
    target = tanggal or datetime.utcnow().strftime("%Y-%m-%d")
    data = service.get_timings(latitude, longitude, metode, target)
    if not data:
        row = db.query(JadwalSholat).filter(JadwalSholat.tanggal == target).first()
        if not row:
            raise HTTPException(status_code=404, detail="Jadwal sholat tidak tersedia.")
        return _to_out(row)
    # simpan ke DB
    row = db.query(JadwalSholat).filter(JadwalSholat.tanggal == target).first()
    lokasi = f"{latitude},{longitude}"
    if not row:
        row = JadwalSholat(
            tanggal=target, subuh=data.get("subuh"), dzuhur=data.get("dzuhur"),
            ashar=data.get("ashar"), maghrib=data.get("maghrib"), isya=data.get("isya"),
            lokasi=lokasi, latitude=latitude, longitude=longitude, metode=metode,
            diperbarui_pada=datetime.utcnow(),
        )
        db.add(row)
    else:
        row.subuh = data.get("subuh"); row.dzuhur = data.get("dzuhur")
        row.ashar = data.get("ashar"); row.maghrib = data.get("maghrib"); row.isya = data.get("isya")
        row.lokasi = lokasi; row.latitude = latitude; row.longitude = longitude; row.metode = metode
        row.diperbarui_pada = datetime.utcnow()
    db.commit()
    db.refresh(row)
    return _to_out(row)


@router.get("/jadwal/{tanggal}", response_model=PrayerTimeOut)
def jadwal_tanggal(tanggal: str, db: Session = Depends(get_db)):
    row = db.query(JadwalSholat).filter(JadwalSholat.tanggal == tanggal).first()
    if not row:
        raise HTTPException(status_code=404, detail="Jadwal untuk tanggal tersebut tidak tersimpan.")
    return _to_out(row)


@router.get("/preferensi", response_model=PrayerPreferencesOut)
def get_preferensi(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    pref = db.query(PrayerPreferences).filter(PrayerPreferences.user_id == current_user.id).first()
    if not pref:
        pref = PrayerPreferences(user_id=current_user.id)
        db.add(pref)
        db.commit()
        db.refresh(pref)
    return pref


@router.put("/preferensi", response_model=PrayerPreferencesOut)
def set_preferensi(
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
