"""Inisialisasi database SQLite dengan SQLAlchemy."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from utils.constants import DB_DIR, DB_NAME

Base = declarative_base()


def get_database_path(app_user_data_dir=None) -> str:
    """Menentukan path file database. Menggunakan app_user_data_dir jika tersedia
    (untuk Android), jika tidak fallback ke direktori pengguna."""
    if app_user_data_dir:
        return os.path.join(app_user_data_dir, DB_NAME)
    os.makedirs(DB_DIR, exist_ok=True)
    return os.path.join(DB_DIR, DB_NAME)


_engine = None
_Session = None


def init_db(app_user_data_dir=None):
    global _engine, _Session
    db_path = get_database_path(app_user_data_dir)
    _engine = create_engine(f"sqlite:///{db_path}", echo=False, future=True)
    Base.metadata.create_all(_engine)
    _Session = sessionmaker(bind=_engine, autoflush=False, autocommit=False, future=True)
    return db_path


def get_session():
    if _Session is None:
        raise RuntimeError("Database belum diinisialisasi. Panggil init_db terlebih dahulu.")
    return _Session()


def dispose_db():
    global _engine, _Session
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _Session = None
