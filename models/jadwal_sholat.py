"""Model Jadwal Sholat dan preferensi."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.db import Base


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
    user_id = Column(Integer, nullable=True)
    lokasi = Column(String(200), nullable=True)
    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)
    metode = Column(String(50), nullable="mwml")
    zona_waktu = Column(String(100), nullable="Asia/Jakarta")
    pengingat_aktif = Column(Boolean, default=True)
    pengingat_offset = Column(Integer, default=0)  # menit sebelumnya
    suara_aktif = Column(Boolean, default=True)
    getaran_aktif = Column(Boolean, default=True)
