"""Router kumpulan doa."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import KategoriDoa, Doa, FavoriteDoa, User
from backend.auth import get_current_user
from backend.schemas import KategoriDoaOut, DoaOut

router = APIRouter(prefix="/doa", tags=["Doa"])


@router.get("/kategori", response_model=list[KategoriDoaOut])
def daftar_kategori(db: Session = Depends(get_db)):
    return db.query(KategoriDoa).all()


@router.get("", response_model=list[DoaOut])
def daftar_doa(
    kategori: str | None = Query(None),
    q: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user),
):
    query = db.query(Doa)
    if kategori:
        query = query.join(KategoriDoa).filter(KategoriDoa.nama == kategori)
    if q:
        like = f"%{q}%"
        query = query.filter((Doa.judul.ilike(like)) | (Doa.terjemahan.ilike(like)))
    daftar = query.all()
    result = []
    for d in daftar:
        is_fav = False
        if current_user:
            is_fav = (
                db.query(FavoriteDoa)
                .filter(FavoriteDoa.user_id == current_user.id, FavoriteDoa.doa_id == d.id)
                .first()
            ) is not None
        result.append(DoaOut(
            id=d.id, kategori_id=d.kategori_id, judul=d.judul, arab=d.arab,
            latin=d.latin, terjemahan=d.terjemahan, referensi=d.referensi,
            is_favorit=is_fav,
        ))
    return result


@router.get("/{doa_id}", response_model=DoaOut)
def detail_doa(
    doa_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user),
):
    d = db.query(Doa).filter(Doa.id == doa_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Doa tidak ditemukan.")
    is_fav = False
    if current_user:
        is_fav = (
            db.query(FavoriteDoa)
            .filter(FavoriteDoa.user_id == current_user.id, FavoriteDoa.doa_id == doa_id)
            .first()
        ) is not None
    return DoaOut(
        id=d.id, kategori_id=d.kategori_id, judul=d.judul, arab=d.arab,
        latin=d.latin, terjemahan=d.terjemahan, referensi=d.referensi,
        is_favorit=is_fav,
    )


@router.post("/{doa_id}/favorit")
def toggle_favorit_doa(
    doa_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.is_guest:
        raise HTTPException(status_code=400, detail="Favorit tidak tersedia untuk tamu.")
    existing = (
        db.query(FavoriteDoa)
        .filter(FavoriteDoa.user_id == current_user.id, FavoriteDoa.doa_id == doa_id)
        .first()
    )
    if existing:
        db.delete(existing)
        db.commit()
        return {"favorit": False, "message": "Dihapus dari favorit."}
    db.add(FavoriteDoa(user_id=current_user.id, doa_id=doa_id))
    db.commit()
    return {"favorit": True, "message": "Ditambahkan ke favorit."}
