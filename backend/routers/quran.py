"""Router Al-Qur'an dan surah."""

import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Surah, FavoriteSurah, User
from backend.auth import get_current_user
from backend.schemas import SurahOut
from backend.utils.constants import API_QURAN_SURAH

router = APIRouter(prefix="/quran", tags=["Al-Qur'an"])


@router.get("/surah", response_model=list[SurahOut])
def daftar_surah(
    q: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user),
):
    query = db.query(Surah).order_by(Surah.nomor)
    if q:
        like = f"%{q}%"
        query = query.filter((Surah.nama_latin.ilike(like)) | (Surah.nama_arab.ilike(like)))
    daftar = query.all()
    result = []
    for s in daftar:
        is_fav = False
        if current_user:
            is_fav = (
                db.query(FavoriteSurah)
                .filter(FavoriteSurah.user_id == current_user.id, FavoriteSurah.surah_id == s.id)
                .first()
            ) is not None
        result.append(SurahOut(
            id=s.id, nomor=s.nomor, nama_arab=s.nama_arab, nama_latin=s.nama_latin,
            arti=s.arti, jumlah_ayat=s.jumlah_ayat, jenis=s.jenis, is_favorit=is_fav,
        ))
    return result


@router.get("/surah/{surah_id}", response_model=SurahOut)
def detail_surah(
    surah_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user),
):
    s = db.query(Surah).filter(Surah.id == surah_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Surah tidak ditemukan.")
    is_fav = False
    if current_user:
        is_fav = (
            db.query(FavoriteSurah)
            .filter(FavoriteSurah.user_id == current_user.id, FavoriteSurah.surah_id == surah_id)
            .first()
        ) is not None
    return SurahOut(
        id=s.id, nomor=s.nomor, nama_arab=s.nama_arab, nama_latin=s.nama_latin,
        arti=s.arti, jumlah_ayat=s.jumlah_ayat, jenis=s.jenis, is_favorit=is_fav,
    )


@router.post("/surah/{surah_id}/favorit")
def toggle_favorit_surah(
    surah_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.is_guest:
        raise HTTPException(status_code=400, detail="Favorit tidak tersedia untuk tamu.")
    existing = (
        db.query(FavoriteSurah)
        .filter(FavoriteSurah.user_id == current_user.id, FavoriteSurah.surah_id == surah_id)
        .first()
    )
    if existing:
        db.delete(existing)
        db.commit()
        return {"favorit": False, "message": "Dihapus dari favorit."}
    db.add(FavoriteSurah(user_id=current_user.id, surah_id=surah_id))
    db.commit()
    return {"favorit": True, "message": "Ditambahkan ke favorit."}


@router.get("/api/surah")
def ambil_surah_api():
    """Ambil daftar surah dari API eksternal equran.id (fallback)."""
    try:
        resp = requests.get(API_QURAN_SURAH, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status"):
            return data["data"]
        return {"error": "Data surah tidak tersedia dari API."}
    except Exception as exc:
        return {"error": str(exc)}
