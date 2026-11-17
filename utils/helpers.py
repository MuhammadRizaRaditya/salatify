"""Fungsi bantu umum."""

from datetime import datetime
import pytz


def get_current_datetime(timezone_str: str = "Asia/Jakarta"):
    try:
        tz = pytz.timezone(timezone_str)
    except Exception:
        tz = pytz.UTC
    return datetime.now(tz)


def format_time(dt) -> str:
    return dt.strftime("%H:%M")


def format_date_indonesia(dt) -> str:
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
             "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    return f"{hari[dt.weekday()]}, {dt.day} {bulan[dt.month - 1]} {dt.year}"


def countdown_to(target_time_str: str, now=None):
    """Menghitung sisa waktu dalam detik hingga target_time_str (HH:MM) hari ini."""
    if now is None:
        from datetime import datetime as _dt
        now = _dt.now()
    try:
        target = datetime.strptime(target_time_str, "%H:%M").time()
    except Exception:
        return None
    from datetime import datetime as _dt
    target_dt = _dt.combine(now.date(), target, tzinfo=now.tzinfo)
    delta = (target_dt - now).total_seconds()
    if delta < 0:
        return None
    return int(delta)


def format_countdown(seconds: int) -> str:
    if seconds is None or seconds < 0:
        return "--:--"
    menit = int(seconds // 60)
    detik = int(seconds % 60)
    jam = menit // 60
    menit = menit % 60
    if jam > 0:
        return f"{jam:02d}:{menit:02d}:{detik:02d}"
    return f"{menit:02d}:{detik:02d}"
