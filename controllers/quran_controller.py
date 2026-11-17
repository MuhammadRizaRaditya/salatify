"""Controller Al-Qur'an: daftar surah, pencarian, favorit."""

from database.db import get_session
from models.surah import Surah, FavoriteSurah


class QuranController:
    def __init__(self, user_id=None):
        self.session = get_session()
        self.user_id = user_id

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
