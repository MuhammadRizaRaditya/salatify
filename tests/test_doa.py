"""Unit tests untuk kumpulan doa."""

import unittest
import tempfile
import os

from database.db import init_db, get_session
from database.seed import run_seed
from controllers.doa_controller import DoaController


class TestDoa(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        init_db(self.tmpdir)
        self.session = get_session()
        run_seed(self.session)
        self.ctrl = DoaController(user_id=1)

    def test_daftar_kategori(self):
        kat = self.ctrl.daftar_kategori()
        self.assertGreater(len(kat), 0)

    def test_daftar_doa(self):
        daftar = self.ctrl.daftar_doa()
        self.assertGreater(len(daftar), 0)

    def test_pencarian(self):
        hasil = self.ctrl.daftar_doa(q="makan")
        self.assertGreater(len(hasil), 0)

    def test_favorit_toggle(self):
        doa = self.ctrl.daftar_doa()[0]
        self.assertFalse(self.ctrl.is_favorit(doa.id))
        added = self.ctrl.toggle_favorit(doa.id)
        self.assertTrue(added)
        self.assertTrue(self.ctrl.is_favorit(doa.id))
        removed = self.ctrl.toggle_favorit(doa.id)
        self.assertFalse(removed)

    def tearDown(self):
        self.session.close()
        from database.db import dispose_db
        dispose_db()


if __name__ == "__main__":
    unittest.main()
