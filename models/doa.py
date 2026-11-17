"""Model Doa dan Kategori Doa."""

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base


class KategoriDoa(Base):
    __tablename__ = "kategori_doa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(100), unique=True, nullable=False)
    label = Column(String(100), nullable=False)

    doa = relationship("Doa", back_populates="kategori", cascade="all, delete-orphan")


class Doa(Base):
    __tablename__ = "doa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    kategori_id = Column(Integer, ForeignKey("kategori_doa.id", ondelete="CASCADE"), nullable=False)
    judul = Column(String(200), nullable=False)
    arab = Column(Text, nullable=False)
    latin = Column(Text, nullable=True)
    terjemahan = Column(Text, nullable=True)
    referensi = Column(Text, nullable=True)
    diverifikasi = Column(Integer, default=1)

    kategori = relationship("KategoriDoa", back_populates="doa")


class FavoriteDoa(Base):
    __tablename__ = "favorite_doa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    doa_id = Column(Integer, ForeignKey("doa.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="doa_favorit")
