# Analisis Kebutuhan — SALATIFY

## 1. Tujuan
Membuat aplikasi Android pendamping ibadah harian untuk umat Islam dengan fitur jadwal sholat, pengingat, arah kiblat, dzikir, doa, dan murottal Al-Qur'an dalam satu aplikasi.

## 2. Pengguna (Actor)
- Pengguna Terdaftar (login dengan username/email/password)
- Pengguna Tamu (fitur dasar tanpa akun)

## 3. Fungsi Utama (Use Case)
| Use Case | Deskripsi |
|---|---|
| Registrasi & Login | Buat akun, masuk, keluar, simpan sesi |
| Dashboard | Lihat salam, tanggal, jam, jadwal sholat, countdown |
| Jadwal Sholat | Lihat jadwal 5 waktu, atur lokasi & metode, simpan offline |
| Pengingat Sholat | Notifikasi lokal waktu sholat & peringatan sebelumnya |
| Arah Kiblat | Kompas digital, arah kiblat, derajat, kalibrasi |
| Dzikir & Tasbih | Baca dzikir, hitung tasbih, simpan riwayat |
| Kumpulan Doa | Cari, filter, detail, favorit, salin doa |
| Al-Qur'an | Daftar surah, putar audio murottal, favorit |
| Pengaturan | Profil, notifikasi, suara, getaran, tema, tentang |

## 3. Keuntungan Non-Fungsional
- Android Native-style (Kivy/KivyMD), bukan web.
- Orientasi portrait.
- Bahasa Indonesia.
- Password di-hash; tidak ada teks biasa.
- Data disimpan di SQLite lokal (user_data_dir).
- Izin hanya yang digunakan: INTERNET, lokasi, notifikasi, getaran, jaringan.

## 4. Kendala
- Build APK membutuhkan WSL2 Ubuntu (Buildozer tidak berjalan native di Windows).
- Fitur sensor (GPS, kompas) dan notifikasi memerlukan pengujian pada perangkat Android fisik/emulator.
- Python 3.14 menggunakan Kivy 2.3.2 / KivyMD 2.0.0 (versi terbaru yang tersedia untuk cp314).
