"""Unit tests untuk jadwal sholat dan countdown."""

import unittest
import tempfile
import os

from database.db import init_db, get_session
from controllers.prayer_controller import PrayerController
from utils.helpers import countdown_to, format_countdown


class TestPrayer(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        init_db(self.tmpdir)
        self.session = get_session()
        self.ctrl = PrayerController(user_id=1)

    def test_countdown(self):
        detik = countdown_to("23:59")
        self.assertIsNotNone(detik)
        teks = format_countdown(detik)
        self.assertIn(":", teks)

    def test_jadwal_offline_kosong(self):
        data = self.ctrl.jadwal_offline("2025-01-01")
        self.assertIsNone(data)

    def tearDown(self):
        self.session.close()
        from database.db import dispose_db
        dispose_db()


if __name__ == "__main__":
    unittest.main()
