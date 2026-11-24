"""Router kumpulan doa."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import KategoriDoa, Doa, FavoriteDoa, User
from backend.schemas import KategoriDoaOut, DoaOut

router = APIRouter(prefix="/doa", tags=["Doa"])


@router.get("/kategori", response_model=list[KategoriDoaOut])
def daftar_kategori_public(db: Session = Depends(get_db)):
    """Endpoint publik: daftar kategori doa."""
    return db.query(KategoriDoa).all()


@router.get("", response_model=list[DoaOut])
def daftar_doa_public(
    kategori: str | None = Query(None),
    q: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """Endpoint publik: list doa dengan filter kategori dan pencarian."""
    query = db.query(Doa)
    if kategori:
        query = query.join(KategoriDoa).filter(KategoriDoa.nama == kategori)
    if q:
        like = f"%{q}%"
        query = query.filter((Doa.judul.ilike(like)) | (Doa.terjemahan.ilike(like)))
    daftar = query.all()
    result = []
    for d in daftar:
        result.append(DoaOut(
            id=d.id, kategori_id=d.kategori_id, judul=d.judul, arab=d.arab,
            latin=d.latin, terjemahan=d.terjemahan, referensi=d.referensi,
        ))
    return result


@router.get("/{doa_id}", response_model=DoaOut)
def detail_doa_public(
    doa_id: int,
    db: Session = Depends(get_db),
):
    """Endpoint publik: detail doa."""
    d = db.query(Doa).filter(Doa.id == doa_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Doa tidak ditemukan.")
    return DoaOut(
        id=d.id, kategori_id=d.kategori_id, judul=d.judul, arab=d.arab,
        latin=d.latin, terjemahan=d.terjemahan, referensi=d.referensi,
    )


@router.post("/{doa_id}/favorit")
def toggle_favorit_doa(
    doa_id: int,
    db: Session = Depends(get_db),
):
    """Endpoint favorit (butuh login/tamu)."""
    pass  # Favorit butuh auth, dipisahkan dari endpoint publik