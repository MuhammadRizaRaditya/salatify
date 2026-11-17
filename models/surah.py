"""Model Surah dan favorit surah."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base


class Surah(Base):
    __tablename__ = "surah"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nomor = Column(Integer, unique=True, nullable=False)
    nama_arab = Column(String(100), nullable=False)
    nama_latin = Column(String(100), nullable=False)
    arti = Column(String(100), nullable=True)
    jumlah_ayat = Column(Integer, nullable=True)
    jenis = Column(String(20), nullable=True)  # Makkiyah / Madaniyah


class FavoriteSurah(Base):
    __tablename__ = "favorite_surah"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    surah_id = Column(Integer, ForeignKey("surah.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="surah_favorit")
