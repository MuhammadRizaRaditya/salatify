"""Unit tests untuk dzikir dan tasbih."""

import unittest
import tempfile
import os

from database.db import init_db, get_session
from controllers.dzikir_controller import DzikirController


class TestDzikir(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        init_db(self.tmpdir)
        self.session = get_session()
        self.ctrl = DzikirController(user_id=1)

    def test_daftar_dzikir(self):
        daftar = self.ctrl.daftar_dzikir(kategori="tasbih")
        self.assertIsInstance(daftar, list)

    def test_simpan_riwayat(self):
        ok = self.ctrl.simpan_tasbih(33, dzikir_id=None)
        self.assertTrue(ok)
        riwayat = self.ctrl.riwayat(limit=5)
        self.assertGreaterEqual(len(riwayat), 1)

    def tearDown(self):
        self.session.close()
        from database.db import dispose_db
        dispose_db()


if __name__ == "__main__":
    unittest.main()
