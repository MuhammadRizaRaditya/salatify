"""Service audio murottal via Plyer / Android MediaPlayer (fallback)."""

try:
    from plyer import audio  # mungkin tidak tersedia di semua platform
except Exception:
    audio = None


class AudioService:
    def __init__(self):
        self._playing = False
        self._current_url = None

    def play(self, url):
        """Mulai pemutaran audio. Kembalikan True jika berhasil memicu play."""
        try:
            if audio:
                audio.play(url)
            self._playing = True
            self._current_url = url
            return True
        except Exception as exc:
            print(f"[AudioService] gagal play: {exc}")
            self._playing = False
            return False

    def stop(self):
        try:
            if audio:
                audio.stop()
        except Exception:
            pass
        self._playing = False
        self._current_url = None

    @property
    def playing(self):
        return self._playing
