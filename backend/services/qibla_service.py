"""Service perhitungan bearing kiblat untuk backend."""

import math
from backend.utils.constants import KAABAH_LATITUDE, KAABAH_LONGITUDE


class QiblaService:
    def bearing_kiblat(self, lat_user, lon_user):
        try:
            lat1 = math.radians(float(lat_user))
            lon1 = math.radians(float(lon_user))
            lat2 = math.radians(KAABAH_LATITUDE)
            lon2 = math.radians(KAABAH_LONGITUDE)
        except (TypeError, ValueError):
            return None
        delta_lon = lon2 - lon1
        x = math.sin(delta_lon) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)
        bearing = math.degrees(math.atan2(x, y))
        bearing = (bearing + 360) % 360
        return round(bearing, 2)
