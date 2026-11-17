"""Service jadwal sholat untuk backend (API Aladhan)."""

import requests
from backend.utils.constants import API_PRAYER_TIMES, DEFAULT_CALC_METHOD


class PrayerService:
    def __init__(self, timeout=15):
        self.timeout = timeout

    def get_timings(self, latitude, longitude, metode=DEFAULT_CALC_METHOD, tanggal=None):
        params = {"latitude": latitude, "longitude": longitude, "method": metode}
        if tanggal:
            params["date"] = tanggal
        try:
            resp = requests.get(API_PRAYER_TIMES, params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            if data.get("code") != 200:
                return None
            timings = data["data"]["timings"]
            return {
                "subuh": timings.get("Fajr"),
                "dzuhur": timings.get("Dhuhr"),
                "ashar": timings.get("Asr"),
                "maghrib": timings.get("Maghrib"),
                "isya": timings.get("Isha"),
            }
        except Exception:
            return None
