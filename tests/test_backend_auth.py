"""Unit tests for backend API authentication routes."""

import os
os.environ["SALATIFY_ENV"] = "development"
os.environ["SALATIFY_SECRET_KEY"] = "test-dev-key-must-be-at-least-32-chars-long!"

import unittest
from datetime import timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi import HTTPException
from backend.auth import decode_token, create_access_token
from backend.database import Base
from backend.models import User
from backend.routers.auth import login_guest, register
from backend.schemas import UserRegister


class TestBackendAuth(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite://")
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def test_guest_login_creates_new_user_each_call(self):
        """Setiap panggilan guest menghasilkan user berbeda."""
        first = login_guest(self.session)
        second = login_guest(self.session)

        self.assertEqual(
            self.session.query(User).filter_by(is_guest=True).count(), 2
        )
        self.assertNotEqual(
            decode_token(first["access_token"])["sub"],
            decode_token(second["access_token"])["sub"],
        )

    def test_guest_cannot_login_via_login_endpoint(self):
        """Guest tidak bisa login lewat /auth/login."""
        guest_token = login_guest(self.session)
        guest_user_id = decode_token(guest_token["access_token"])["sub"]
        user = self.session.query(User).filter_by(id=guest_user_id).first()
        self.assertTrue(user.is_guest)

    def test_register_rejects_tamu_prefix(self):
        """Register menolak username yang dimulai 'tamu-'."""
        payload = UserRegister(username="tamu-abc", email="tamu-abc@example.com", password="password123")
        with self.assertRaises(HTTPException) as ctx:
            register(payload, self.session)
        self.assertEqual(ctx.exception.status_code, 400)

        # Register dengan email palsu juga harus ditolak (validasi username/email policy)
        payload2 = UserRegister(username="user2", email="tamu@guest.salatify.local", password="password123")
        with self.assertRaises(HTTPException) as ctx:
            register(payload2, self.session)
        self.assertEqual(ctx.exception.status_code, 400)

    def test_register_rejects_blocked_usernames(self):
        """Register menolak username cadangan: tamu, guest, admin, root, salatify."""
        blocked = ["tamu", "guest", "admin", "root", "salatify"]
        for blocked_username in blocked:
            payload = UserRegister(username=blocked_username, email=f"{blocked_username}@example.com", password="password123")
            with self.assertRaises(HTTPException) as ctx:
                register(payload, self.session)
            self.assertEqual(ctx.exception.status_code, 400)

    def test_guest_token_has_expiry(self):
        """Token tamu punya field exp di payload."""
        guest_token = login_guest(self.session)
        decoded = decode_token(guest_token["access_token"])
        self.assertIsNotNone(decoded)
        self.assertIn("exp", decoded)


    def tearDown(self):
        self.session.close()
        self.engine.dispose()


if __name__ == "__main__":
    unittest.main()