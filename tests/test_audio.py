"""Unit tests untuk fitur audio murottal (mock requests, tanpa jaringan asli)."""

import unittest
import os
import tempfile
import time
from unittest.mock import patch

from sqlalchemy import create_engine, text

from database.db import init_db, get_session, dispose_db, _migrate_surah_audio_url
from models.surah import Surah
from services.audio_service import AudioService, ERR_OFFLINE, ERR_TIMEOUT, ERR_NOT_FOUND


class _MockResp:
    def __init__(self, json_data=None, exc=None):
        self._json = json_data or {}
        self._exc = exc

    def raise_for_status(self):
        if self._exc:
            raise self._exc

    def json(self):
        return self._json

    def iter_content(self, chunk_size=8192):
        if self._exc:
            raise self._exc
        yield b"audio-chunk-data"


def _patch_get(mock_resp):
    return patch("services.audio_service.requests.get", return_value=mock_resp)


class TestAudioMigration(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.tmpdir, "salatify.db")
        init_db(self.tmpdir)
        self.session = get_session()

    def test_kolom_audio_url_ada_setelah_init_db(self):
        engine = create_engine(f"sqlite:///{self.db_path}")
        with engine.connect() as conn:
            cols = [r[1] for r in conn.execute(text("PRAGMA table_info(surah)")).fetchall()]
        self.assertIn("audio_url", cols)

    def test_migrasi_kolom_audio_url_pada_db_lama(self):
        old_db = os.path.join(self.tmpdir, "lama.db")
        engine = create_engine(f"sqlite:///{old_db}")
        with engine.connect() as conn:
            conn.execute(text("""CREATE TABLE surah (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nomor INTEGER UNIQUE NOT NULL,
                nama_arab VARCHAR(100) NOT NULL,
                nama_latin VARCHAR(100) NOT NULL,
                arti VARCHAR(100),
                jumlah_ayat INTEGER,
                jenis VARCHAR(20)
            )"""))
            conn.commit()
        with engine.connect() as conn:
            cols_before = [r[1] for r in conn.execute(text("PRAGMA table_info(surah)")).fetchall()]
        self.assertNotIn("audio_url", cols_before)

        _migrate_surah_audio_url(engine)

        with engine.connect() as conn:
            cols_after = [r[1] for r in conn.execute(text("PRAGMA table_info(surah)")).fetchall()]
        self.assertIn("audio_url", cols_after)

    def tearDown(self):
        self.session.close()
        dispose_db()


class TestAudioUrl(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        init_db(self.tmpdir)
        self.session = get_session()
        self.svc = AudioService(app_user_data_dir=self.tmpdir)
        s = Surah(nomor=1, nama_arab="الفاتحة", nama_latin="Al-Fatihah",
                  arti="Pembuka", jumlah_ayat=7, jenis="Makkiyah")
        self.session.add(s)
        self.session.commit()

    def test_get_audio_url_dari_api_dan_simpan_ke_db(self):
        url = "https://cdn.equran.id/audio-full/Abdullah-Al-Juhany/001.mp3"
        with _patch_get(_MockResp(json_data={"data": {"audioFull": {"01": url}}})):
            hasil = self.svc.get_audio_url(1)
        self.assertEqual(hasil, url)
        simpan = self.session.query(Surah).filter_by(nomor=1).first()
        self.assertIsNotNone(simpan.audio_url)
        self.assertEqual(simpan.audio_url, url)

    def test_get_audio_url_dari_db_tanpa_api(self):
        url = "https://cdn.equran.id/audio-full/Abdullah-Al-Juhany/001.mp3"
        s = Surah(nomor=2, nama_arab="البقرة", nama_latin="Al-Baqarah",
                  arti="Sapi", jumlah_ayat=286, jenis="Madaniyah", audio_url=url)
        self.session.add(s)
        self.session.commit()
        with patch("services.audio_service.requests.get") as mock_get:
            hasil = self.svc.get_audio_url(2)
        self.assertEqual(hasil, url)
        mock_get.assert_not_called()

    def test_get_audio_url_api_gagal_tanpa_crash(self):
        with patch("services.audio_service.requests.get",
                   side_effect=Exception("jaringan mati")):
            hasil = self.svc.get_audio_url(1)
        self.assertIsNone(hasil)

    def tearDown(self):
        self.session.close()
        dispose_db()


class TestAudioDownload(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        init_db(self.tmpdir)
        self.session = get_session()
        self.svc = AudioService(app_user_data_dir=self.tmpdir)
        s = Surah(nomor=1, nama_arab="الفاتحة", nama_latin="Al-Fatihah",
                  arti="Pembuka", jumlah_ayat=7, jenis="Makkiyah",
                  audio_url="https://cdn.equran.id/audio-full/Abdullah-Al-Juhany/001.mp3")
        self.session.add(s)
        self.session.commit()

    def _tunggu_selesai(self, detik_maks=5):
        for _ in range(int(detik_maks * 20)):
            if self.svc._downloading.get(1) is None:
                return
            time.sleep(0.05)

    def test_download_sukses_file_mp3_tersimpan_part_dibersihkan(self):
        url = "https://cdn.equran.id/audio-full/Abdullah-Al-Juhany/001.mp3"
        with _patch_get(_MockResp(json_data={"data": {"audioFull": {"01": url}}})):
            self.svc.download_audio(1)
            self._tunggu_selesai()
        self.assertTrue(self.svc.is_downloaded(1))
        self.assertFalse(os.path.exists(self.svc.local_path(1) + ".part"))

    def test_download_timeout_status_gagal(self):
        import requests
        with patch("services.audio_service.requests.get",
                   side_effect=requests.Timeout("timeout")):
            self.svc.download_audio(1)
            self._tunggu_selesai()
        self.assertEqual(self.svc.status, "gagal")
        self.assertEqual(self.svc.error, ERR_TIMEOUT)

    def test_download_offline_status_gagal(self):
        import requests
        with patch("services.audio_service.requests.get",
                   side_effect=requests.ConnectionError("offline")):
            self.svc.download_audio(1)
            self._tunggu_selesai()
        self.assertEqual(self.svc.status, "gagal")
        self.assertEqual(self.svc.error, ERR_OFFLINE)

    def tearDown(self):
        self.session.close()
        dispose_db()


class TestAudioPlayOffline(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        init_db(self.tmpdir)
        self.session = get_session()
        self.svc = AudioService(app_user_data_dir=self.tmpdir)
        self.status = None
        self.error = None
        self.svc.add_listener(lambda s, e: setattr(self, "status", s) or setattr(self, "error", e))

    def test_play_offline_tidak_crash_dan_tampilkan_pesan_error(self):
        with patch("services.audio_service.requests.get",
                   side_effect=Exception("tidak ada internet")):
            self.svc.play(1)
        time.sleep(0.3)
        self.assertEqual(self.svc.status, "gagal")
        self.assertIsNotNone(self.svc.error)
        self.assertFalse(self.svc.playing)

    def test_pause_resume_stop_tidak_crash_saat_tidak_memutar(self):
        self.svc.pause()
        self.svc.resume()
        self.svc.stop()
        self.assertFalse(self.svc.playing)

    def tearDown(self):
        self.session.close()
        dispose_db()


if __name__ == "__main__":
    unittest.main()
