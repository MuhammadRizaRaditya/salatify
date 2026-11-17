"""Controller kumpulan doa: daftar, pencarian, filter, favorit, detail."""

from database.db import get_session
from models.doa import KategoriDoa, Doa, FavoriteDoa


class DoaController:
    def __init__(self, user_id=None):
        self.session = get_session()
        self.user_id = user_id

    def daftar_kategori(self):
        return self.session.query(KategoriDoa).all()

    def daftar_doa(self, kategori=None, q=None):
        query = self.session.query(Doa)
        if kategori:
            query = query.join(KategoriDoa).filter(KategoriDoa.nama == kategori)
        if q:
            like = f"%{q}%"
            query = query.filter(
                (Doa.judul.like(like)) | (Doa.terjemahan.like(like))
            )
        return query.all()

    def detail(self, doa_id):
        return self.session.query(Doa).filter_by(id=doa_id).first()

    def is_favorit(self, doa_id):
        if not self.user_id:
            return False
        return self.session.query(FavoriteDoa).filter_by(
            user_id=self.user_id, doa_id=doa_id
        ).first() is not None

    def toggle_favorit(self, doa_id):
        if not self.user_id:
            return False
        existing = self.session.query(FavoriteDoa).filter_by(
            user_id=self.user_id, doa_id=doa_id
        ).first()
        if existing:
            self.session.delete(existing)
            self.session.commit()
            return False
        self.session.add(FavoriteDoa(user_id=self.user_id, doa_id=doa_id))
        self.session.commit()
        return True
