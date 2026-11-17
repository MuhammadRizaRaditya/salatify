"""Model Dzikir dan riwayat tasbih."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.db import Base


class Dzikir(Base):
    __tablename__ = "dzikir"

    id = Column(Integer, primary_key=True, autoincrement=True)
    kategori = Column(String(50), nullable=False)
    judul = Column(String(200), nullable=False)
    arab = Column(Text, nullable=False)
    latin = Column(Text, nullable=True)
    terjemahan = Column(Text, nullable=True)
    jumlah_dianjurkan = Column(Integer, nullable=True)


class DzikirHistory(Base):
    __tablename__ = "dzikir_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    dzikir_id = Column(Integer, nullable=True)
    jumlah = Column(Integer, default=0)
    tanggal = Column(DateTime, default=datetime.now, nullable=False)

    user = relationship("User", back_populates="dzikir_history")
