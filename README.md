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

## Class Diagram

Diagram kelas lengkap dalam format Mermaid terlihat di bawah ini. Diagram ditampilkan langsung di halaman repository GitHub karena menggunakan sintaks meraval yang didukung GitHub.

### Diagram Model (Database)

```mermaid
direction TB
classDiagram
    class User {
        +id: int PK
        +username: varchar(100) unique
        +email: varchar(150) unique
        +password_hash: varchar(255)
        +is_guest: bool default false
        +is_active: bool default true
        +created_at: datetime
    }
    class JadwalSholat {
        +id: int PK
        +tanggal: varchar(20)
        +subuh: varchar(10)
        +dzuhur: varchar(10)
        +ashar: varchar(10)
        +maghrib: varchar(10)
        +isya: varchar(10)
        +lokasi: varchar(200)
        +latitude: varchar(50)
        +longitude: varchar(50)
        +metode: varchar(50)
        +perbarui_pada: datetime
    }
    class PrayerPreferences {
        +id: int PK
        +user_id: int FK unique
        +lokasi: varchar(200)
        +latitude: varchar(50)
        +longitude: varchar(50)
        +metode: varchar(50)
        +zona_waktu: varchar(100)
        +pengingat_aktif: bool default true
        +pengingat_offset: int default 0
        +suara_aktif: bool default true
        +getaran_aktif: bool default true
    }
    class KategoriDoa {
        +id: int PK
        +nama: varchar(100) unique
        +label: varchar(100)
    }
    class Doa {
        +id: int PK
        +kategori_id: int FK
        +judul: varchar(200)
        +arab: text
        +latin: text
        +terjemahan: text
        +referensi: text
        +diverifikasi: int default 1
    }
    class FavoriteDoa {
        +id: int PK
        +user_id: int FK
        +doa_id: int FK
    }
    class Dzikir {
        +id: int PK
        +kategori: varchar(50)
        +judul: varchar(200)
        +arab: text
        +latin: text
        +terjemahan: text
        +jumlah_dianjurkan: int
    }
    class DzikirHistory {
        +id: int PK
        +user_id: int FK
        +dzikir_id: int
        +jumlah: int default 0
        +tanggal: datetime
    }
    class Surah {
        +id: int PK
        +nomor: int unique
        +nama_arab: varchar(100)
        +nama_latin: varchar(100)
        +arti: varchar(100)
        +jumlah_ayat: int
        +jenis: varchar(20)
    }
    class FavoriteSurah {
        +id: int PK
        +user_id: int FK
        +surah_id: int FK
    }
    class UserSettings {
        +id: int PK
        +user_id: int FK unique
        +tema_gelap: bool default false
        +nama_lengkap: varchar(150)
        +email: varchar(150)
    }

    User "1" *-- "*" FavoriteDoa : doa_favorit
    User "1" *-- "*" FavoriteSurah : surah_favorit
    User "1" *-- "*" DzikirHistory : dzikir_history
    User "1" -- "*" PrayerPreferences : preferensi
    User "1" -- "*" UserSettings : settingan
    KategoriDoa "1" *-- "*" Doa : doa
    Doa "N" -- "1" KategoriDoa : kategori
    FavoriteDoa "N" -- "1" User : user
    FavoriteDoa "N" -- "1" Doa : doa
    DzikirHistory "N" -- "1" User : user
    DzikirHistory "N" -- "0..1" Dzikir : dzikir (opsional)
    FavoriteSurah "N" -- "1" User : user
    FavoriteSurah "N" -- "1" Surah : surah
    Surah "1" *-- "*" FavoriteSurah : favorit
    PrayerPreferences "1" -- "1" User : user
    UserSettings "1" -- "1" User : user
```

### Diagram Controller & Service

```mermaid
direction LR
classDiagram
    class AuthController {
        +register(username, email, password): bool
        +login(username_or_email, password): bool
        +login_guest(): bool
        +logout(): bool
        +change_password(old_password, new_password): bool
    }
    class DashboardController {
        +salam(nama): str
        +tanggal_masehi(): str
        +tanggal_hijriah(): str
        +jam_digital(): str
        +jadwal_hari_ini(lat, lon, metode): dict
        +countdown_berikutnya(jadwal): tuple
        +ringkasan_dzikir(): int
    }
    class PrayerController {
        +get_preferences(): PrayerPreferences
        +save_preferences(lokasi, lat, lon, metode, zona_waktu, pengingat_aktif, offset, suara, getaran): PrayerPreferences
        +ambil_jadwal(lat, lon, metode, tanggal): dict
        +jadwal_offline(tanggal): dict
        +hitung_countdown(waktu_str): str
    }
    class QiblaController {
        +hitung_bearing(lat_user, lon_user): float
        +arah_teks(derajat): str
    }
    class DzikirController {
        +daftar_dzikir(kategori=None): list
        +simpan_tasbih(jumlah, dzikir_id): bool
        +riwayat(limit=20): list
    }
    class DoaController {
        +daftar_kategori(): list
        +daftar_doa(kategori=None, q=None): list
        +detail(doa_id): Doa
        +is_favorit(doa_id): bool
        +toggle_favorit(doa_id): bool
    }
    class QuranController {
        +daftar_surah(q=None): list
        +detail(surah_id): Surah
        +toggle_favorit(surah_id): bool
    }
    class PrayerService {
        +get_timings(latitude, longitude, metode, tanggal): dict
    }
    class QiblaService {
        +bearing_kiblat(lat_user, lon_user): float
    }
    class LocationService {
        +start(): bool
        +stop(): None
    }
    class NotificationService {
        +kirim(judul, pesan, timeout): bool
        +pengingat_sholat(nama_sholat, waktu): bool
    }
    class QuranService {
        +daftar_surah(): list
    }
    class AudioService {
        +play(url): bool
        +stop(): None
        +playing: bool
    }

    AuthController ..> PrayerService : gunakan
    DashboardController ..> PrayerService : gunakan
    DashboardController ..> DzikirHistory : query
    PrayerController ..> PrayerService : gunakan
    PrayerController ..> PrayerPreferences : query/save
    PrayerController ..> JadwalSholat : query/save
    QiblaController ..> QiblaService : gunakan
    QiblaController ..> LocationService : ambil lokasi
    DzikirController ..> Dzikir : query
    DzikirController ..> User : query history
    DzikirController ..> DzikirHistory : simpan/query
    DoaController ..> KategoriDoa : query
    DoaController ..> Doa : query
    DoaController ..> FavoriteDoa : toggle favorit
    DoaController ..> User : cek user_id
    QuranController ..> QuranService : ambil data
    QuranController ..> FavoriteSurah : toggle favorit
    QuranController ..> Surah : query
    QuranController ..> AudioService : play murottal
    AuthController ..> SalatifyApiClient : (opsional) sync ke backend
```

### Diagram View (Screen)

```mermaid
direction LR
classDiagram
    class SplashScreen
    class LoginScreen
    class RegisterScreen
    class DashboardScreen
    class PrayerScreen
    class QiblaScreen
    class DzikirScreen
    class DoaScreen
    class QuranScreen
    class SettingsScreen

    SplashScreen --> LoginScreen : pindah setelah 3 detik
    LoginScreen --> DashboardScreen : login sukses
    RegisterScreen --> LoginScreen : daftar akun baru
    DashboardScreen --> AuthController : salam, jam, jadwal
    PrayerScreen --> PrayerController : jadwal, countdown, preferensi
    QiblaScreen --> QiblaController : bearing, arah kiblat
    QiblaScreen --> LocationService : sensor GPS
    DzikirScreen --> DzikirController : tasbih, riwayat
    DoaScreen --> DoaController : daftar doa, favorit, detail
    QuranScreen --> QuranController : daftar surah, favorit, audio
    QuranScreen --> AudioService : play murottal
    SettingsScreen --> AuthController : logout, tema, profil
```

### Lengkap ke docs/class_diagram.md

Untuk diagram lengkap dengan penjelasan tambahan, kunjungi: [docs/class_diagram.md](https://github.com/MuhammadRizaRaditya/salatify/blob/main/docs/class_diagram.md)

---

## Database (SQLite + SQLAlchemy)

Tabel: `users`, `kategori_doa`, `doa`, `favorite_doa`, `dzikir`, `dzikir_history`, `jadwal_sholat`, `prayer_preferences`, `user_settings`, `surah`, `favorite_surah`.

Database otomatis dibuat pada `app_user_data_dir` (Android) atau direktori pengguna (desktop). Password tidak disimpan sebagai teks biasa. Seeder idempoten (tidak duplikasi saat dijalankan berulang).

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

## Versi Website

SALATIFY sekarang juga memiliki versi website yang dapat diakses melalui browser Google Chrome dan Microsoft Edge. Versi website menggunakan:

- **Frontend**: HTML, CSS, JavaScript (responsive design, PWA)
- **Backend**: FastAPI (Python) dengan JWT authentication
- **Database**: PostgreSQL (produksi) / SQLite (development)
- **Fitur**: Semua 15 fitur terintegrasi, termasuk landing page, dashboard, jadwal sholat, kiblat, dzikir, doa, Al-Qur'an, dan pengaturan

### Cara Menjalankan Website

Lihat dokumentasi lengkap di `docs/running_local.md`:
- Backend FastAPI: `cd backend && uvicorn main:app --port 8000`
- Website: Buka `http://127.0.0.1:8000/web/index.html` atau file HTML langsung
- API Docs: `http://127.0.0.1:8000/docs`

### Integrasi dengan Aplikasi Android

Adapter API tersedia di `services/api_client.py`. Aplikasi Android tetap berjalan lokal dengan SQLite, adapter opsional untuk sinkronisasi ke backend.

### Deployment

Lihat `docs/running_local.md` untuk panduan deployment ke Render, Heroku, atau VPS.

## Lisensi

Dikembangkan oleh Hasan, Luqman, Riza, dan Wisnu.
