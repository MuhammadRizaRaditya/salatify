"""Unit tests for backend API authentication routes."""

import os
os.environ["SALATIFY_ENV"] = "development"
os.environ["SALATIFY_SECRET_KEY"] = "test-dev-key-must-be-at-least-32-chars-long!"

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.auth import decode_token
from backend.database import Base
from backend.models import User
from backend.routers.auth import login_guest


class TestBackendAuth(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite://")
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def test_guest_login_reuses_existing_account(self):
        first = login_guest(self.session)
        second = login_guest(self.session)

        self.assertEqual(self.session.query(User).filter_by(is_guest=True).count(), 1)
        self.assertEqual(
            decode_token(first["access_token"])["sub"],
            decode_token(second["access_token"])["sub"],
        )

    def tearDown(self):
        self.session.close()
        self.engine.dispose()


if __name__ == "__main__":
    unittest.main()
