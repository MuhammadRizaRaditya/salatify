"""Model pengaturan pengguna dan tema."""

from sqlalchemy import Column, Integer, String, Boolean
from database.db import Base


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    tema_gelap = Column(Boolean, default=False)
    nama_lengkap = Column(String(150), nullable=True)
    email = Column(String(150), nullable=True)
