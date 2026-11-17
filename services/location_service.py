"""Service akses lokasi perangkat via Plyer (GPS)."""

from plyer import gps


class LocationService:
    def __init__(self, on_location=None, on_status=None):
        self.on_location = on_location
        self.on_status = on_status
        self._started = False

    def start(self):
        try:
            gps.configure(on_location=self._on_location, on_status=self._on_status)
            gps.start(minTime=1000, minDistance=0)
            self._started = True
            return True
        except Exception as exc:
            if self.on_status:
                self.on_status(f"GPS tidak tersedia: {exc}")
            return False

    def stop(self):
        try:
            gps.stop()
        except Exception:
            pass
        self._started = False

    def _on_location(self, **kwargs):
        if self.on_location:
            self.on_location(kwargs)

    def _on_status(self, stype, message):
        if self.on_status:
            self.on_status(message)
