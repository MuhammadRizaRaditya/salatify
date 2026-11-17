"""Router dzikir dan riwayat tasbih."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Dzikir, DzikirHistory, User
from backend.auth import get_current_user
from backend.schemas import DzikirOut, DzikirHistoryIn, DzikirHistoryOut

router = APIRouter(prefix="/dzikir", tags=["Dzikir"])


@router.get("", response_model=list[DzikirOut])
def daftar_dzikir(kategori: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Dzikir)
    if kategori:
        query = query.filter(Dzikir.kategori == kategori)
    return query.all()


@router.get("/riwayat", response_model=list[DzikirHistoryOut])
def riwayat_dzikir(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if current_user.is_guest:
        return []
    return (
        db.query(DzikirHistory)
        .filter(DzikirHistory.user_id == current_user.id)
        .order_by(DzikirHistory.tanggal.desc())
        .all()
    )


@router.post("/riwayat", response_model=DzikirHistoryOut)
def simpan_tasbih(
    payload: DzikirHistoryIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.is_guest:
        raise HTTPException(status_code=400, detail="Riwayat tidak tersedia untuk tamu.")
    from datetime import datetime, timezone
    history = DzikirHistory(
        user_id=current_user.id,
        dzikir_id=payload.dzikir_id,
        jumlah=payload.jumlah,
        tanggal=datetime.now(timezone.utc),
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history
