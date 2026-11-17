"""Model SQLAlchemy untuk backend SALATIFY (PostgreSQL).
Mirror model aplikasi Android agar business logic dan data dapat digunakan bersama."""

import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_guest = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    doa_favorit = relationship("FavoriteDoa", back_populates="user", cascade="all, delete-orphan")
    surah_favorit = relationship("FavoriteSurah", back_populates="user", cascade="all, delete-orphan")
    dzikir_history = relationship("DzikirHistory", back_populates="user", cascade="all, delete-orphan")
    prayer_pref = relationship("PrayerPreferences", back_populates="user", uselist=False, cascade="all, delete-orphan")
    settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_guest": self.is_guest,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


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


class Dzikir(Base):
    __tablename__ = "dzikir"

    id = Column(Integer, primary_key=True, autoincrement=True)
    kategori = Column(String(50), nullable=False)
    judul = Column(String(200), nullable=False)
    arab = Column(Text, nullable=False)
    latin = Column(Text, nullable=True)
    terjemahan = Column(Text, nullable=True)
    jumlah_dianjurkan = Column(Integer, nullable=True)


class DzikirHistory(Base):
    __tablename__ = "dzikir_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    dzikir_id = Column(Integer, nullable=True)
    jumlah = Column(Integer, default=0)
    tanggal = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="dzikir_history")


class JadwalSholat(Base):
    __tablename__ = "jadwal_sholat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tanggal = Column(String(20), nullable=False)  # YYYY-MM-DD
    subuh = Column(String(10), nullable=True)
    dzuhur = Column(String(10), nullable=True)
    ashar = Column(String(10), nullable=True)
    maghrib = Column(String(10), nullable=True)
    isya = Column(String(10), nullable=True)
    lokasi = Column(String(200), nullable=True)
    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)
    metode = Column(String(50), nullable=True)
    diperbarui_pada = Column(DateTime, nullable=True)


class PrayerPreferences(Base):
    __tablename__ = "prayer_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    lokasi = Column(String(200), nullable=True)
    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)
    metode = Column(String(50), nullable=True, default="mwml")
    zona_waktu = Column(String(100), nullable=True, default="Asia/Jakarta")
    pengingat_aktif = Column(Boolean, default=True)
    pengingat_offset = Column(Integer, default=0)
    suara_aktif = Column(Boolean, default=True)
    getaran_aktif = Column(Boolean, default=True)

    user = relationship("User", back_populates="prayer_pref")


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    tema_gelap = Column(Boolean, default=False)
    nama_lengkap = Column(String(150), nullable=True)
    email = Column(String(150), nullable=True)

    user = relationship("User", back_populates="settings")


class Surah(Base):
    __tablename__ = "surah"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nomor = Column(Integer, unique=True, nullable=False)
    nama_arab = Column(String(100), nullable=False)
    nama_latin = Column(String(100), nullable=False)
    arti = Column(String(100), nullable=True)
    jumlah_ayat = Column(Integer, nullable=True)
    jenis = Column(String(20), nullable=True)


class FavoriteSurah(Base):
    __tablename__ = "favorite_surah"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    surah_id = Column(Integer, ForeignKey("surah.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="surah_favorit")
