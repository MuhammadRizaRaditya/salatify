"""Model User."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_guest = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=None)

    doa_favorit = relationship("FavoriteDoa", back_populates="user", cascade="all, delete-orphan")
    surah_favorit = relationship("FavoriteSurah", back_populates="user", cascade="all, delete-orphan")
    dzikir_history = relationship("DzikirHistory", back_populates="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_guest": self.is_guest,
            "is_active": self.is_active,
        }
