"""Controller autentikasi: registrasi, login, logout, sesi."""

from database.db import get_session
from models.user import User
from utils.security import hash_password, verify_password
from utils.validators import is_valid_email, is_valid_password, validate_required


class AuthController:
    def __init__(self, app_user_data_dir=None):
        from database.db import init_db
        init_db(app_user_data_dir)
        self.session = get_session()
        self.current_user = None

    def register(self, username, email, password):
        ok, msg = validate_required(username, "Username")
        if not ok:
            return False, msg
        ok, msg = validate_required(email, "Email")
        if not ok:
            return False, msg
        if not is_valid_email(email):
            return False, "Format email tidak valid."
        ok, msg = is_valid_password(password)
        if not ok:
            return False, msg

        if self.session.query(User).filter_by(username=username).first():
            return False, "Username sudah digunakan."
        if self.session.query(User).filter_by(email=email).first():
            return False, "Email sudah terdaftar."

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            is_guest=False,
            is_active=True,
        )
        self.session.add(user)
        self.session.commit()
        return True, "Registrasi berhasil. Silakan login."

    def login(self, username_or_email, password):
        ok, msg = validate_required(username_or_email, "Username/Email")
        if not ok:
            return False, msg
        ok, msg = validate_required(password, "Password")
        if not ok:
            return False, msg

        user = (
            self.session.query(User)
            .filter((User.username == username_or_email) | (User.email == username_or_email))
            .first()
        )
        if not user or not verify_password(password, user.password_hash):
            return False, "Username/Email atau password salah."
        if not user.is_active:
            return False, "Akun tidak aktif."
        self.current_user = user
        return True, f"Selamat datang, {user.username}."

    def login_guest(self):
        user = User(
            username="tamu",
            email="tamu@salatify.local",
            password_hash=hash_password("guest"),
            is_guest=True,
            is_active=True,
        )
        self.session.add(user)
        self.session.commit()
        self.current_user = user
        return True, "Mode tamu diaktifkan. Fitur dasar tersedia."

    def logout(self):
        self.current_user = None
        return True, "Anda telah keluar."

    def change_password(self, old_password, new_password):
        if not self.current_user or self.current_user.is_guest:
            return False, "Tidak tersedia untuk tamu."
        if not verify_password(old_password, self.current_user.password_hash):
            return False, "Password lama salah."
        ok, msg = is_valid_password(new_password)
        if not ok:
            return False, msg
        self.current_user.password_hash = hash_password(new_password)
        self.session.commit()
        return True, "Password berhasil diubah."
