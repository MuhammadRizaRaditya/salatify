"""Controller dashboard: salam, tanggal, jadwal, countdown, ringkasan dzikir."""

from datetime import datetime
from database.db import get_session
from models.user import User
from models.dzikir import DzikirHistory
from models.jadwal_sholat import JadwalSholat
from utils.helpers import get_current_datetime, format_date_indonesia, countdown_to, format_countdown


class DashboardController:
    def __init__(self, user_id=None, timezone_str="Asia/Jakarta"):
        self.session = get_session()
        self.user_id = user_id
        self.timezone_str = timezone_str

    def salam(self, nama=None):
        now = get_current_datetime(self.timezone_str)
        jam = now.hour
        if 4 <= jam < 11:
            s = "Pagi"
        elif 11 <= jam < 15:
            s = "Siang"
        elif 15 <= jam < 18:
            s = "Sore"
        else:
            s = "Malam"
        panggilan = nama if nama else "Pengguna"
        return f"Selamat {s}, {panggilan}"

    def tanggal_masehi(self):
        now = get_current_datetime(self.timezone_str)
        return format_date_indonesia(now)

    def tanggal_hijriah(self):
        # Implementasi sederhana tanpa dependensi eksternal berat.
        now = get_current_datetime(self.timezone_str)
        return now.strftime("1 %b %Y")  # placeholder, diformat oleh view

    def jam_digital(self):
        now = get_current_datetime(self.timezone_str)
        return now.strftime("%H:%M:%S")

    def jadwal_hari_ini(self, latitude, longitude, metode="mwml"):
        today = get_current_datetime(self.timezone_str).strftime("%Y-%m-%d")
        row = (
            self.session.query(JadwalSholat)
            .filter_by(tanggal=today)
            .first()
        )
        if row:
            return {
                "subuh": row.subuh,
                "dzuhur": row.dzuhur,
                "ashar": row.ashar,
                "maghrib": row.maghrib,
                "isya": row.isya,
            }
        return {}

    def countdown_berikutnya(self, jadwal):
        now = get_current_datetime(self.timezone_str)
        urutan = ["subuh", "dzuhur", "ashar", "maghrib", "isya"]
        for nama in urutan:
            waktu = jadwal.get(nama)
            if waktu:
                sisa = countdown_to(waktu, now)
                if sisa is not None:
                    return nama, sisa, waktu
        return None, None, None

    def ringkasan_dzikir(self):
        if not self.user_id:
            return 0
        total = (
            self.session.query(DzikirHistory)
            .filter_by(user_id=self.user_id)
            .count()
        )
        return total
