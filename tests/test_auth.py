"""Unit tests untuk autentikasi."""

import unittest
import tempfile
import os

from database.db import init_db, get_session, Base
from controllers.auth_controller import AuthController
from utils.security import hash_password, verify_password
from utils.validators import is_valid_email, is_valid_password


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.tmpdir, "test.db")
        init_db(self.tmpdir)
        self.auth = AuthController(self.tmpdir)

    def test_hash_password_not_plaintext(self):
        hashed = hash_password("rahasia123")
        self.assertNotEqual(hashed, "rahasia123")
        self.assertTrue(verify_password("rahasia123", hashed))
        self.assertFalse(verify_password("salah", hashed))

    def test_register_and_login(self):
        ok, msg = self.auth.register("hasan", "hasan@mail.com", "password123")
        self.assertTrue(ok, msg)
        ok, msg = self.auth.login("hasan", "password123")
        self.assertTrue(ok, msg)
        self.assertIsNotNone(self.auth.current_user)

    def test_login_wrong_password(self):
        self.auth.register("luqman", "luqman@mail.com", "password123")
        ok, msg = self.auth.login("luqman", "salah")
        self.assertFalse(ok)

    def test_register_duplicate_email(self):
        self.auth.register("riz", "riz@mail.com", "password123")
        ok, msg = self.auth.register("riz2", "riz@mail.com", "password123")
        self.assertFalse(ok)

    def test_validators(self):
        self.assertTrue(is_valid_email("a@b.com"))
        self.assertFalse(is_valid_email("tidakvalid"))
        ok, msg = is_valid_password("123456")
        self.assertTrue(ok)
        ok, msg = is_valid_password("123")
        self.assertFalse(ok)

    def test_guest_login(self):
        ok, msg = self.auth.login_guest()
        self.assertTrue(ok)
        self.assertTrue(self.auth.current_user.is_guest)

    def tearDown(self):
        self.auth.session.close()
        from database.db import dispose_db
        dispose_db()


if __name__ == "__main__":
    unittest.main()
