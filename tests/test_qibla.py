"""Unit tests untuk kompas kiblat."""

import unittest
from controllers.qibla_controller import QiblaController


class TestQibla(unittest.TestCase):
    def setUp(self):
        self.ctrl = QiblaController()

    def test_bearing_jakarta(self):
        derajat = self.ctrl.hitung_bearing(-6.2, 106.8)
        self.assertIsNotNone(derajat)
        self.assertGreaterEqual(derajat, 0)
        self.assertLess(derajat, 360)

    def test_arah_teks(self):
        self.assertEqual(self.ctrl.arah_teks(0), "Utara")
        self.assertEqual(self.ctrl.arah_teks(90), "Timur")
        self.assertEqual(self.ctrl.arah_teks(180), "Selatan")
        self.assertEqual(self.ctrl.arah_teks(270), "Barat")
        self.assertEqual(self.ctrl.arah_teks(None), "--")


if __name__ == "__main__":
    unittest.main()
