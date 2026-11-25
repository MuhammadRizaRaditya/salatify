"""Service audio murottal Al-Qur'an.

Unduh file MP3 ke penyimpanan aplikasi lalu putar secara lokal (tidak
stream langsung dari URL agar stabil di Android). Semua error ditangkap dan
diubah menjadi pesan Indonesia yang jelas; aplikasi tidak crash meski offline.
"""

from __future__ import annotations

import os
import threading
from typing import Callable, Optional, Tuple

import requests
from sqlalchemy.orm import Session

from database.db import get_session
from models.surah import Surah
from utils.constants import API_QURAN_SURAH_DETAIL

# Kunci qari default dalam data.audioFull equran.id ("01" = Abdullah Al-Juhany).
DEFAULT_QARI_KEY = "01"

# Pesan error dalam bahasa Indonesia.
ERR_OFFLINE = "Tidak ada koneksi internet. Muatan audio tidak dapat diunduh."
ERR_TIMEOUT = "Waktu unduhan habis. Coba kembali nanti."
ERR_CORRUPT = "File audio rusak atau tidak dapat diputar."
ERR_PLAY = "Gagal memutar audio."
ERR_NOT_FOUND = "Data surah atau URL audio tidak tersedia."

try:  # Kivy tidak tersedia di environment pengembangan tanpa kivy.
    from kivy.core.audio import SoundLoader  # type: ignore
    from kivy.clock import Clock  # type: ignore
except Exception:  # pragma: no cover - hanya untuk pengembangan tanpa kivy
    SoundLoader = None  # type: ignore
    Clock = None  # type: ignore


class AudioService:
    """Pengelola unduhan dan pemutaran audio murottal."""

    def __init__(self, app_user_data_dir: Optional[str] = None):
        self.app_user_data_dir = app_user_data_dir or os.path.expanduser("~")
        self.audio_dir = os.path.join(self.app_user_data_dir, "audio")
        os.makedirs(self.audio_dir, exist_ok=True)

        self._sound = None
        self._playing = False
        self._current_nomor: Optional[int] = None
        self._current_url: Optional[str] = None
        self._volume = 0.8
        self._downloading: dict = {}  # nomor -> bool
        self._error: Optional[str] = None
        self._status = "siap"
        self._listeners: list[Callable[[str, Optional[str]], None]] = []
        self._lock = threading.Lock()

    # ---------- status / listener ----------
    @property
    def status(self) -> str:
        return self._status

    @property
    def error(self) -> Optional[str]:
        return self._error

    @property
    def playing(self) -> bool:
        return self._playing

    @property
    def volume(self) -> float:
        return self._volume

    def add_listener(self, callback: Callable[[str, Optional[str]], None]) -> None:
        self._listeners.append(callback)

    def _emit(self, status: str, error: Optional[str] = None) -> None:
        self._status = status
        self._error = error
        for cb in list(self._listeners):
            try:
                cb(status, error)
            except Exception:
                pass

    def _run_main(self, callback) -> None:
        """Jalankan callback di main thread jika Kivy tersedia."""
        if Clock is not None:
            Clock.schedule_once(lambda dt: callback())
        else:
            callback()

    # ---------- path & DB ----------
    def local_path(self, nomor_surah: int) -> str:
        return os.path.join(self.audio_dir, f"{nomor_surah:03d}.mp3")

    def is_downloaded(self, nomor_surah: int) -> bool:
        path = self.local_path(nomor_surah)
        return os.path.isfile(path) and os.path.getsize(path) > 0

    def _db_session(self) -> Session:
        return get_session()

    def get_audio_url(self, nomor_surah: int) -> Optional[str]:
        """Ambil URL audio dari DB; jika kosong ambil dari API dan simpan ke DB."""
        session = self._db_session()
        try:
            surah = session.query(Surah).filter_by(nomor=nomor_surah).first()
            if surah and surah.audio_url:
                return surah.audio_url
            url = self._fetch_audio_url_from_api(nomor_surah)
            if url and surah:
                surah.audio_url = url
                session.commit()
                return url
            return url
        except Exception as exc:
            print(f"[AudioService] get_audio_url gagal: {exc}")
            return None
        finally:
            session.close()

    def _fetch_audio_url_from_api(self, nomor_surah: int) -> Optional[str]:
        """Ambil URL mp3 dari equran.id (data.audioFull, qari default)."""
        try:
            resp = requests.get(
                API_QURAN_SURAH_DETAIL.format(nomor_surah), timeout=15
            )
            resp.raise_for_status()
            data = resp.json()
            audio_full = data.get("data", {}).get("audioFull") or {}
            url = audio_full.get(DEFAULT_QARI_KEY)
            if not url and audio_full:
                url = next(iter(audio_full.values()))
            return url
        except Exception as exc:
            print(f"[AudioService] fetch audio URL gagal: {exc}")
            return None

    # ---------- download ----------
    def download_audio(self, nomor_surah: int) -> None:
        """Unduh MP3 ke audio/{nomor}.mp3 di thread terpisah (non-blokir UI)."""
        if self._downloading.get(nomor_surah):
            return
        self._downloading[nomor_surah] = True
        self._emit("mengunduh...")

        thread = threading.Thread(
            target=self._download_thread, args=(nomor_surah,), daemon=True
        )
        thread.start()

    def _download_thread(self, nomor_surah: int) -> None:
        try:
            url = self.get_audio_url(nomor_surah)
            if not url:
                self._run_main(
                    lambda: self._emit(
                        "gagal", ERR_NOT_FOUND
                    )
                )
                return

            part_path = self.local_path(nomor_surah) + ".part"
            final_path = self.local_path(nomor_surah)

            try:
                resp = requests.get(url, timeout=20, stream=True)
                resp.raise_for_status()
                with open(part_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                os.replace(part_path, final_path)
            except requests.Timeout:
                self._run_main(
                    lambda: self._emit("gagal", ERR_TIMEOUT)
                )
                return
            except requests.RequestException:
                self._run_main(
                    lambda: self._emit("gagal", ERR_OFFLINE)
                )
                return
            except Exception:
                self._run_main(
                    lambda: self._emit("gagal", ERR_CORRUPT)
                )
                return

            # Bersihkan sisa .part jika ada.
            if os.path.exists(part_path):
                try:
                    os.remove(part_path)
                except Exception:
                    pass

            self._run_main(
                lambda: (
                    self._downloading.pop(nomor_surah, None),
                    self._emit("siap"),
                )
            )
        except Exception as exc:
            print(f"[AudioService] download thread error: {exc}")
            self._run_main(
                lambda: self._emit("gagal", ERR_CORRUPT)
            )
        finally:
            self._downloading.pop(nomor_surah, None)

    # ---------- play / pause / resume / stop ----------
    def play(self, nomor_surah: int) -> bool:
        """Putar audio surah. Lokal jika sudah ada, unduh dulu jika belum."""
        self.stop()
        self._current_nomor = nomor_surah

        if self.is_downloaded(nomor_surah):
            self._load_and_play(nomor_surah)
            return True

        # Belum terunduh: ambil URL dan unduh, lalu putar saat selesai.
        url = self.get_audio_url(nomor_surah)
        if not url:
            self._emit("gagal", ERR_NOT_FOUND)
            return False

        self._current_url = url
        self._emit("mengunduh...")

        def _selesai_unduh() -> None:
            if self.is_downloaded(nomor_surah):
                self._load_and_play(nomor_surah)
            else:
                self._emit("gagal", ERR_OFFLINE)

        thread = threading.Thread(target=_selesai_unduh, daemon=True)
        thread.start()
        return True

    def _load_and_play(self, nomor_surah: int) -> None:
        def _do() -> None:
            if SoundLoader is None:
                self._emit("gagal", "Pemain audio tidak tersedia di perangkat ini.")
                return
            path = self.local_path(nomor_surah)
            if not os.path.isfile(path):
                self._emit("gagal", "File audio tidak ditemukan.")
                return
            try:
                self._sound = SoundLoader.load(path)
                if self._sound is None:
                    self._emit("gagal", ERR_CORRUPT)
                    return
                self._sound.volume = self._volume
                self._sound.play()
                self._playing = True
                self._emit("memutar")
            except Exception as exc:
                print(f"[AudioService] play error: {exc}")
                self._emit("gagal", ERR_PLAY)

        self._run_main(_do)

    def pause(self) -> None:
        def _do() -> None:
            if self._sound and self._playing:
                try:
                    self._sound.stop()
                except Exception:
                    pass
                self._playing = False
                self._emit("dihentikan")

        self._run_main(_do)

    def resume(self) -> None:
        def _do() -> None:
            if self._sound and not self._playing:
                try:
                    self._sound.play()
                except Exception:
                    pass
                self._playing = True
                self._emit("memutar")

        self._run_main(_do)

    def stop(self) -> None:
        def _do() -> None:
            if self._sound:
                try:
                    self._sound.stop()
                except Exception:
                    pass
                self._sound = None
            self._playing = False
            self._current_nomor = None
            self._current_url = None
            self._emit("dihentikan")

        self._run_main(_do)

    def set_volume(self, value: float) -> None:
        self._volume = max(0.0, min(1.0, float(value)))
        if self._sound:
            try:
                self._sound.volume = self._volume
            except Exception:
                pass

    # ---------- progress ----------
    def progress(self) -> Tuple[float, float]:
        """Kembalikan (posisi, durasi) dalam detik."""
        if self._sound:
            try:
                posisi = self._sound.get_pos()
                durasi = self._sound.length
                if posisi is None:
                    posisi = 0.0
                if durasi is None:
                    durasi = 0.0
                return float(posisi), float(durasi)
            except Exception:
                pass
        return 0.0, 0.0
