"""Controller arah kiblat: hitung bearing dari lokasi pengguna ke Ka'bah."""

import math
from services.qibla_service import QiblaService


class QiblaController:
    def __init__(self):
        self.service = QiblaService()

    def hitung_bearing(self, lat_user, lon_user):
        return self.service.bearing_kiblat(lat_user, lon_user)

    def arah_teks(self, derajat):
        if derajat is None:
            return "--"
        arah = ["Utara", "Timur Laut", "Timur", "Tenggara",
                "Selatan", "Barat Daya", "Barat", "Barat Laut"]
        index = int(((derajat + 22.5) % 360) / 45)
        return arah[index]
