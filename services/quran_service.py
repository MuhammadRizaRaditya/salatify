"""Service data Al-Qur'an (surah) via API equran.id (publik, legal)."""

import requests
from utils.constants import API_QURAN_SURAH


class QuranService:
    def __init__(self, timeout=15):
        self.timeout = timeout

    def daftar_surah(self):
        """Mengembalikan list surah dari API, atau None jika gagal."""
        try:
            resp = requests.get(API_QURAN_SURAH, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            if not data.get("status"):
                return None
            return data["data"]
        except Exception:
            return None
