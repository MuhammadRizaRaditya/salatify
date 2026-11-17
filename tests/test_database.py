"""Unit tests untuk database dan seeder."""

import unittest
import tempfile
import os

from database.db import init_db, get_session
from database.seed import run_seed
from models.user import User
from models.doa import Doa, KategoriDoa, FavoriteDoa
from models.dzikir import Dzikir, DzikirHistory
from models.surah import Surah, FavoriteSurah
from models.jadwal_sholat import JadwalSholat


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        init_db(self.tmpdir)
        self.session = get_session()

    def test_seed_idempotent(self):
        run_seed(self.session)
        count1 = self.session.query(Doa).count()
        run_seed(self.session)
        count2 = self.session.query(Doa).count()
        self.assertEqual(count1, count2)
        self.assertGreater(count1, 0)

    def test_user_crud(self):
        u = User(username="wisnu", email="wisnu@mail.com", password_hash="hash", is_guest=False)
        self.session.add(u)
        self.session.commit()
        found = self.session.query(User).filter_by(username="wisnu").first()
        self.assertIsNotNone(found)
        self.assertEqual(found.email, "wisnu@mail.com")

    def test_doa_favorit_relasi(self):
        run_seed(self.session)
        u = User(username="u1", email="u1@mail.com", password_hash="h")
        self.session.add(u)
        self.session.commit()
        doa = self.session.query(Doa).first()
        fav = FavoriteDoa(user_id=u.id, doa_id=doa.id)
        self.session.add(fav)
        self.session.commit()
        self.assertEqual(u.doa_favorit[0].doa_id, doa.id)

    def test_dzikir_history(self):
        u = User(username="u2", email="u2@mail.com", password_hash="h")
        self.session.add(u)
        self.session.commit()
        h = DzikirHistory(user_id=u.id, dzikir_id=1, jumlah=33)
        self.session.add(h)
        self.session.commit()
        self.assertEqual(u.dzikir_history[0].jumlah, 33)

    def test_surah_favorit(self):
        run_seed(self.session)
        u = User(username="u3", email="u3@mail.com", password_hash="h")
        self.session.add(u)
        self.session.commit()
        s = self.session.query(Surah).first()
        fav = FavoriteSurah(user_id=u.id, surah_id=s.id)
        self.session.add(fav)
        self.session.commit()
        self.assertEqual(u.surah_favorit[0].surah_id, s.id)

    def test_jadwal_sholat(self):
        j = JadwalSholat(tanggal="2025-01-01", subuh="04:30", dzuhur="12:00",
                         ashar="15:30", maghrib="18:00", isya="19:30",
                         lokasi="Jakarta", latitude="-6.2", longitude="106.8",
                         metode="mwml")
        self.session.add(j)
        self.session.commit()
        found = self.session.query(JadwalSholat).filter_by(tanggal="2025-01-01").first()
        self.assertEqual(found.subuh, "04:30")

    def tearDown(self):
        self.session.close()
        from database.db import dispose_db
        dispose_db()


if __name__ == "__main__":
    unittest.main()
