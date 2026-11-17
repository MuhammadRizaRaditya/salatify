"""Skema Pydantic untuk request/response API SALATIFY."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


# ---------- Auth ----------
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_guest: bool
    is_active: bool

    class Config:
        from_attributes = True


# ---------- Doa ----------
class KategoriDoaOut(BaseModel):
    id: int
    nama: str
    label: str

    class Config:
        from_attributes = True


class DoaOut(BaseModel):
    id: int
    kategori_id: int
    judul: str
    arab: str
    latin: Optional[str] = None
    terjemahan: Optional[str] = None
    referensi: Optional[str] = None
    is_favorit: bool = False

    class Config:
        from_attributes = True


# ---------- Dzikir ----------
class DzikirOut(BaseModel):
    id: int
    kategori: str
    judul: str
    arab: str
    latin: Optional[str] = None
    terjemahan: Optional[str] = None
    jumlah_dianjurkan: Optional[int] = None

    class Config:
        from_attributes = True


class DzikirHistoryIn(BaseModel):
    dzikir_id: Optional[int] = None
    jumlah: int


class DzikirHistoryOut(BaseModel):
    id: int
    dzikir_id: Optional[int] = None
    jumlah: int
    tanggal: datetime

    class Config:
        from_attributes = True


# ---------- Jadwal Sholat ----------
class PrayerTimeOut(BaseModel):
    tanggal: str
    subuh: Optional[str] = None
    dzuhur: Optional[str] = None
    ashar: Optional[str] = None
    maghrib: Optional[str] = None
    isya: Optional[str] = None
    lokasi: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    metode: Optional[str] = None


class PrayerPreferencesIn(BaseModel):
    lokasi: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    metode: Optional[str] = "mwml"
    zona_waktu: Optional[str] = "Asia/Jakarta"
    pengingat_aktif: Optional[bool] = True
    pengingat_offset: Optional[int] = 0
    suara_aktif: Optional[bool] = True
    getaran_aktif: Optional[bool] = True


class PrayerPreferencesOut(BaseModel):
    id: int
    user_id: int
    lokasi: Optional[str]
    latitude: Optional[str]
    longitude: Optional[str]
    metode: Optional[str]
    zona_waktu: Optional[str]
    pengingat_aktif: bool
    pengingat_offset: int
    suara_aktif: bool
    getaran_aktif: bool

    class Config:
        from_attributes = True


# ---------- User Settings ----------
class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class UserSettingsIn(BaseModel):
    tema_gelap: Optional[bool] = False
    nama_lengkap: Optional[str] = None
    email: Optional[str] = None


class UserSettingsOut(BaseModel):
    id: int
    user_id: int
    tema_gelap: bool
    nama_lengkap: Optional[str]
    email: Optional[str]

    class Config:
        from_attributes = True


# ---------- Surah ----------
class SurahOut(BaseModel):
    id: int
    nomor: int
    nama_arab: str
    nama_latin: str
    arti: Optional[str] = None
    jumlah_ayat: Optional[int] = None
    jenis: Optional[str] = None
    is_favorit: bool = False

    class Config:
        from_attributes = True


# ---------- Qibla ----------
class QiblaRequest(BaseModel):
    latitude: float
    longitude: float


class QiblaResponse(BaseModel):
    derajat: float
    arah: str
    kaabah_latitude: float
    kaabah_longitude: float
