"""Konstanta aplikasi SALATIFY."""

# Identitas aplikasi
APP_NAME = "SALATIFY"
APP_TAGLINE = "Smart Islamic Companion"
APP_SLOGAN = "Your Daily Worship Companion"
PACKAGE_NAME = "com.hlrw.salatify"
APP_VERSION = "1.0.0"
DEVELOPERS = ["Hasan", "Luqman", "Riza", "Wisnu"]

# Palet warna Islami
COLOR_PRIMARY = "#123F32"
COLOR_SECONDARY = "#1C7055"
COLOR_ACCENT = "#D8B66A"
COLOR_BACKGROUND = "#F7F8F5"
COLOR_SURFACE = "#FFFFFF"
COLOR_TEXT = "#202A25"

# Koordinat Ka'bah (Makkah)
KAABAH_LATITUDE = 21.4225
KAABAH_LONGITUDE = 39.8262

# Waktu sholat
PRAYER_TIMES = ["subuh", "dzuhur", "ashar", "maghrib", "isya"]
PRAYER_LABELS = {
    "subuh": "Subuh",
    "dzuhur": "Dzuhur",
    "ashar": "Ashar",
    "maghrib": "Maghrib",
    "isya": "Isya",
}

# Metode perhitungan sholat
CALCULATION_METHODS = {
    "mwml": "Kementerian Agama RI",
    "isna": "ISNA (Amerika)",
    "makkah": "Majlis Ugama Makkah",
    "karachi": "Majlis Ugama Karachi",
    "tehran": "Institut Geofisik Tehran",
}

DEFAULT_CALC_METHOD = "mwml"

# Kategori dzikir
DHIKIR_CATEGORIES = [
    "setelah_sholat",
    "pagi",
    "petang",
    "tasbih",
    "istighfar",
    "sholawat",
]

# Kategori doa
DOA_CATEGORIES = [
    "sebelum_makan",
    "setelah_makan",
    "sebelum_tidur",
    "bangun_tidur",
    "masuk_rumah",
    "keluar_rumah",
    "masuk_kamar_mandi",
    "keluar_kamar_mandi",
    "bepergian",
    "memohon_ilmu",
    "orang_tua",
    "setelah_sholat",
    "bercermin",
    "saat_hujan",
]

# Path database
import os
DB_DIR = os.path.join(os.path.expanduser("~"), ".salatify")
DB_NAME = "salatify.db"

# API endpoints (sumber publik yang dapat dipercaya)
API_PRAYER_TIMES = "https://api.aladhan.com/v1/timings"
API_QURAN_SURAH = "https://equran.id/api/v2/surah"
API_QURAN_SURAH_DETAIL = "https://equran.id/api/v2/surat/{}"

# Interval notifikasi pengingat (menit)
REMINDER_OFFSETS = [0, 5, 10, 15]
