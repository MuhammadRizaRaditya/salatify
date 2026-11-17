"""Service notifikasi lokal pengingat sholat via Plyer notification.

Catatan: Plyer notification pada Android menggunakan API Android Native.
Izin POST_NOTIFICATIONS diperlukan pada Android 13+.
"""

from plyer import notification


class NotificationService:
    def __init__(self):
        self.channel_id = "com.hlrw.salatify.prayer"

    def kirim(self, judul, pesan, timeout=10):
        try:
            notification.notify(
                title=judul,
                message=pesan,
                app_name="SALATIFY",
                app_icon=None,
                timeout=timeout,
            )
            return True
        except Exception as exc:
            print(f"[NotificationService] gagal: {exc}")
            return False

    def pengingat_sholat(self, nama_sholat, waktu):
        return self.kirim(
            f"Pengingat {nama_sholat}",
            f"Waktu {nama_sholat} akan tiba pukul {waktu}.",
        )
