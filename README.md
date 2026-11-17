# SALATIFY — Smart Islamic Companion

Aplikasi pendamping ibadah umat Islam untuk Android, berbasis Python, Kivy, dan KivyMD.

**Tagline:** Smart Islamic Companion  
**Slogan:** Your Daily Worship Companion  
**Package:** com.hlrw.salatify  
**Versi:** 1.0.0  
**Pengembang:** Hasan, Luqman, Riza, Wisnu  
**Bahasa:** Indonesia  
**Orientasi:** Portrait

## Fitur Utama

1. **Splash Screen** — Logo, nama aplikasi, tagline, animasi, loading ke halaman autentikasi.
2. **Login & Register** — Username, email, password, konfirmasi password, validasi input, hashing password (PBKDF2-SHA256), sesi pengguna, opsi tetap masuk, mode tamu, logout.
3. **Dashboard** — Salam pembuka, tanggal Masehi & Hijriah, jam digital, lokasi, jadwal sholat lima waktu, countdown ke sholat berikutnya, tombol akses cepat, ringkasan aktivitas dzikir.
4. **Jadwal Sholat** — Subuh, Dzuhur, Ashar, Maghrib, Isya; lokasi via latitude/longitude; data dari API Aladhan; metode perhitungan (prioritas Kementerian Agama RI); penyimpanan offline; countdown.
5. **Pengingat Sholat** — Notifikasi lokal setiap waktu sholat, pengingat 5/10/15 menit sebelumnya, aktif/nonaktif per waktu, suara dan getaran.
6. **Arah Kiblat** — Kompas digital, penunjuk utara, penunjuk arah kiblat, derajat arah kiblat, koordinat pengguna, kalibrasi kompas, status sensor. Perhitungan bearing berdasarkan koordinat Ka'bah.
7. **Wirid & Dzikir** — Dzikir setelah sholat, pagi, petang, tasbih, istighfar, sholawat; teks Arab, latin, terjemahan; tasbih digital dengan tombol tambah/reset, target, progres, getaran, riwayat per pengguna.
8. **Kumpulan Doa** — 14 kategori doa, judul, teks Arab, latin, terjemahan Indonesia, referensi; pencarian, filter kategori, detail, favorit, salin teks.
9. **Al-Qur'an & Murottal** — Daftar 114 surah (seeder 10 surah contoh), nomor, nama Arab/latin, arti, jumlah ayat, jenis; pemutar audio play/pause/stop/volume/progres; pencarian dan favorit surah.
10. **Pengaturan** — Profil, ubah nama/email/password, lokasi, metode perhitungan, notifikasi, suara, getaran, tema terang/gelap, informasi aplikasi, tentang pengembang.

## Teknologi

| Teknologi | Fungsi |
|---|---|
| Python 3 | Bahasa utama |
| Kivy 2.3.2 | Framework Android |
| KivyMD 2.0.0 | Komponen UI |
| SQLite + SQLAlchemy 2.1.9 | Database lokal & ORM |
| Buildozer | Build APK |
| Plyer 2.1.0 | Akses fitur perangkat (GPS, notifikasi) |
| Requests 2.34.2 | Komunikasi API |
| passlib 1.7.4 | Hashing password |
| pytz 2024.2 | Zona waktu |

## Arsitektur MVC

Kode dipisahkan menjadi Model, View, Controller, Service, dan Utils:

- `models/` — Tabel database (User, Doa, Dzikir, JadwalSholat, Surah, dll.)
- `views/` — Layar UI (Splash, Login, Register, Dashboard, Prayer, Qibla, Dzikir, Doa, Quran, Settings)
- `controllers/` — Logika antara model dan view (Auth, Dashboard, Prayer, Qibla, Dzikir, Doa, Quran)
- `services/` — Layanan eksternal (Prayer API, Qibla bearing, Lokasi GPS, Notifikasi, Quran API, Audio)
- `database/` — Inisialisasi DB dan seeder
- `utils/` — Konstanta, keamanan, validator, helper

## Struktur Folder

```
salatify/
├── main.py
├── main.kv
├── requirements.txt
├── buildozer.spec
├── README.md
├── .gitignore
├── models/
├── views/
├── controllers/
├── services/
├── database/
├── utils/
├── assets/images
├── assets/icons
├── assets/fonts
├── assets/audio
├── docs/
└── tests/
```

## Database (SQLite + SQLAlchemy)

Tabel: `users`, `kategori_doa`, `doa`, `favorite_doa`, `dzikir`, `dzikir_history`, `jadwal_sholat`, `prayer_preferences`, `user_settings`, `surah`, `favorite_surah`.

Database otomatis dibuat pada `app_user_data_dir` (Android) atau direktori pengguna (desktop). Password tidak disimpan sebagai teks biasa. Seeder idempoten (tidak duplikasi saat dijalankan berulang).

## API yang Digunakan

- [Aladhan Prayer Times API](https://api.aladhan.com/v1/timings) — jadwal sholat.
- [equran.id API](https://equran.id/api/v2/surah) — daftar surah Al-Qur'an.

Jika API tidak tersedia, aplikasi menampilkan data tersimpan secara offline dan pesan bahwa data belum dapat diperbarui.

## Instalasi Dependensi (Desktop)

```bash
python -m pip install -r requirements.txt
```

## Menjalankan Aplikasi (Desktop)

```bash
python main.py
```

## Menjalankan Pengujian

```bash
python -m unittest discover -s tests
```

## Setup WSL2 Ubuntu (untuk Build APK)

Buildozer tidak berjalan natively di Windows. Gunakan WSL2 Ubuntu:

1. Instal WSL2: `wsl --install` ( restart jika diperlukan )
2. Pastikan distro Ubuntu aktif: `wsl --list --verbose`
3. Masuk Ubuntu: `wsl -d Ubuntu`
4. Instal dependensi build:
   ```bash
   sudo apt update
   sudo apt install -y python3-pip openjdk-17-jdk wget git unzip zip build-essential libssl-dev libffi-dev
   python3 -m pip install --upgrade pip buildozer cython
   ```
5. Salin folder proyek ke Ubuntu atau mount drive Windows.
6. Jalankan build:
   ```bash
   buildozer android debug
   ```

## Build APK

```bash
buildozer android debug
```

File APK hasil build disimpan di `bin/salatify-1.0.0-debug.apk`.

> Catatan: Pada environment pengembangan ini (Windows + Python 3.14), WSL2 Ubuntu belum tersedia (hanya distro docker-desktop yang terhenti). APK belum dibangun pada mesin ini. Untuk hasil APK final, ikuti langkah setup WSL2 Ubuntu di atas dan jalankan `buildozer android debug`.

## Instal APK pada Android

1. Aktifkan "Instal dari sumber tidak dikenal" pada pengaturan Android.
2. Salin `salatify-1.0.0-debug.apk` ke smartphone.
3. Buka file APK dan pilih Instal.
4. Berikan izin lokasi dan notifikasi saat diminta.

## Pengujian yang Dilakukan

- Unit test: 22 tes (auth, database, qibla, dzikir, doa, prayer) — semua lulus.
- Smoke test desktop: semua 11 layar termuat, registrasi/login, seeder database.
- Fitur yang memerlukan perangkat Android fisik (GPS, kompas, notifikasi lokal, murottal audio, pengingat background) belum diuji pada mesin ini dan memerlukan pengujian pada smartphone/emulator Android.

## Catatan Keamanan

- Password di-hash dengan PBKDF2-SHA256, tidak disimpan sebagai teks biasa.
- Password tidak ditampilkan di database atau log.
- Data pengguna terpisah per user_id.

## Lisensi

Dikembangkan oleh Hasan, Luqman, Riza, dan Wisnu.
