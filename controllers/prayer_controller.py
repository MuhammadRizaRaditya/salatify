"""Controller jadwal sholat: ambil, simpan, hitung countdown."""

from database.db import get_session
from models.jadwal_sholat import JadwalSholat, PrayerPreferences
from services.prayer_service import PrayerService
from utils.helpers import countdown_to, format_countdown
from datetime import datetime


class PrayerController:
    def __init__(self, user_id=None):
        self.session = get_session()
        self.user_id = user_id
        self.service = PrayerService()

    def get_preferences(self):
        return self.session.query(PrayerPreferences).first()

    def save_preferences(self, lokasi, latitude, longitude, metode, zona_waktu,
                         pengingat_aktif, offset, suara, getaran):
        pref = self.get_preferences()
        if not pref:
            pref = PrayerPreferences(user_id=self.user_id)
            self.session.add(pref)
        pref.lokasi = lokasi
        pref.latitude = latitude
        pref.longitude = longitude
        pref.metode = metode
        pref.zona_waktu = zona_waktu
        pref.pengingat_aktif = pengingat_aktif
        pref.pengingat_offset = offset
        pref.suara_aktif = suara
        pref.getaran_aktif = getaran
        self.session.commit()
        return pref

    def ambil_jadwal(self, latitude, longitude, metode, tanggal=None):
        data = self.service.get_timings(latitude, longitude, metode, tanggal)
        if data and tanggal:
            self._simpan_jadwal(tanggal, latitude, longitude, metode, data)
        return data

    def _simpan_jadwal(self, tanggal, latitude, longitude, metode, data):
        row = self.session.query(JadwalSholat).filter_by(tanggal=tanggal).first()
        lokasi = f"{latitude},{longitude}"
        if not row:
            row = JadwalSholat(
                tanggal=tanggal,
                subuh=data.get("subuh"),
                dzuhur=data.get("dzuhur"),
                ashar=data.get("ashar"),
                maghrib=data.get("maghrib"),
                isya=data.get("isya"),
                lokasi=lokasi,
                latitude=str(latitude),
                longitude=str(longitude),
                metode=metode,
                diperbarui_pada=datetime.now(),
            )
            self.session.add(row)
        else:
            row.subuh = data.get("subuh")
            row.dzuhur = data.get("dzuhur")
            row.ashar = data.get("ashar")
            row.maghrib = data.get("maghrib")
            row.isya = data.get("isya")
            row.lokasi = lokasi
            row.latitude = str(latitude)
            row.longitude = str(longitude)
            row.metode = metode
            row.diperbarui_pada = datetime.now()
        self.session.commit()

    def jadwal_offline(self, tanggal):
        row = self.session.query(JadwalSholat).filter_by(tanggal=tanggal).first()
        if not row:
            return None
        return {
            "subuh": row.subuh,
            "dzuhur": row.dzuhur,
            "ashar": row.ashar,
            "maghrib": row.maghrib,
            "isya": row.isya,
            "lokasi": row.lokasi,
            "metode": row.metode,
        }

    def hitung_countdown(self, waktu_str):
        from utils.helpers import countdown_to, format_countdown
        detik = countdown_to(waktu_str)
        return format_countdown(detik)
