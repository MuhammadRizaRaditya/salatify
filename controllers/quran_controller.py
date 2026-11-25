"""Controller Al-Qur'an: daftar surah, pencarian, favorit, dan audio murottal."""

from typing import Optional

from database.db import get_session
from models.surah import Surah, FavoriteSurah
from services.audio_service import AudioService


class QuranController:
    def __init__(self, user_id=None, audio_service: Optional[AudioService] = None):
        self.session = get_session()
        self.user_id = user_id
        self.audio = audio_service or AudioService()

    def daftar_surah(self, q=None):
        query = self.session.query(Surah).order_by(Surah.nomor)
        if q:
            like = f"%{q}%"
            query = query.filter(
                (Surah.nama_latin.like(like)) | (Surah.nama_arab.like(like))
            )
        return query.all()

    def detail(self, surah_id):
        return self.session.query(Surah).filter_by(id=surah_id).first()

    def detail_by_nomor(self, nomor: int):
        return self.session.query(Surah).filter_by(nomor=nomor).first()

    def is_favorit(self, surah_id):
        if not self.user_id:
            return False
        return self.session.query(FavoriteSurah).filter_by(
            user_id=self.user_id, surah_id=surah_id
        ).first() is not None

    def toggle_favorit(self, surah_id):
        if not self.user_id:
            return False
        existing = self.session.query(FavoriteSurah).filter_by(
            user_id=self.user_id, surah_id=surah_id
        ).first()
        if existing:
            self.session.delete(existing)
            self.session.commit()
            return False
        self.session.add(FavoriteSurah(user_id=self.user_id, surah_id=surah_id))
        self.session.commit()
        return True

    # ---------- Audio murottal ----------
    def get_audio_url(self, nomor_surah: int):
        return self.audio.get_audio_url(nomor_surah)

    def is_downloaded(self, nomor_surah: int) -> bool:
        return self.audio.is_downloaded(nomor_surah)

    def download_audio(self, nomor_surah: int) -> None:
        self.audio.download_audio(nomor_surah)

    def play_surah(self, nomor_surah: int) -> bool:
        return self.audio.play(nomor_surah)

    def pause_surah(self) -> None:
        self.audio.pause()

    def resume_surah(self) -> None:
        self.audio.resume()

    def stop_surah(self) -> None:
        self.audio.stop()

    def set_volume(self, value: float) -> None:
        self.audio.set_volume(value)

    def progress(self):
        return self.audio.progress()

    @property
    def status(self) -> str:
        return self.audio.status

    @property
    def error(self):
        return self.audio.error

    @property
    def playing(self) -> bool:
        return self.audio.playing

    def add_listener(self, callback):
        self.audio.add_listener(callback)
