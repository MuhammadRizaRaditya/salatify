"""Controller wirid dan dzikir + riwayat tasbih."""

from database.db import get_session
from models.dzikir import Dzikir, DzikirHistory
from models.user import User
from datetime import datetime


class DzikirController:
    def __init__(self, user_id=None):
        self.session = get_session()
        self.user_id = user_id

    def daftar_dzikir(self, kategori=None):
        query = self.session.query(Dzikir)
        if kategori:
            query = query.filter_by(kategori=kategori)
        return query.all()

    def simpan_tasbih(self, jumlah, dzikir_id=None):
        if not self.user_id:
            return False
        history = DzikirHistory(
            user_id=self.user_id,
            dzikir_id=dzikir_id,
            jumlah=jumlah,
            tanggal=datetime.now(),
        )
        self.session.add(history)
        self.session.commit()
        return True

    def riwayat(self, limit=20):
        if not self.user_id:
            return []
        return (
            self.session.query(DzikirHistory)
            .filter_by(user_id=self.user_id)
            .order_by(DzikirHistory.tanggal.desc())
            .limit(limit)
            .all()
        )
