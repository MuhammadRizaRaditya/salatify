# Class Diagram (Ringkasan)

## Model (database.db.Base)
- **User**: id, username, email, password_hash, is_guest, is_active, created_at
  - Relasi: FavoriteDoa (1:N), FavoriteSurah (1:N), DzikirHistory (1:N)
- **KategoriDoa**: id, nama, label
  - Relasi: Doa (1:N)
- **Doa**: id, kategori_id(FK), judul, arab, latin, terjemahan, referensi, diverifikasi
  - Relasi: KategoriDoa (N:1), FavoriteDoa (1:N)
- **FavoriteDoa**: id, user_id(FK), doa_id(FK)
- **Dzikir**: id, kategori, judul, arab, latin, terjemahan, jumlah_dianjurkan
- **DzikirHistory**: id, user_id(FK), dzikir_id, jumlah, tanggal
  - Relasi: User (N:1)
- **JadwalSholat**: id, tanggal, subuh, dzuhur, ashar, maghrib, isya, lokasi, latitude, longitude, metode, diperbarui_pada
- **PrayerPreferences**: id, user_id, lokasi, latitude, longitude, metode, zona_waktu, pengingat_aktif, pengingat_offset, suara_aktif, getaran_aktif
- **UserSettings**: id, user_id, tema_gelap, nama_lengkap, email
- **Surah**: id, nomor, nama_arab, nama_latin, arti, jumlah_ayat, jenis
  - Relasi: FavoriteSurah (1:N)
- **FavoriteSurah**: id, user_id(FK), surah_id(FK)

## Controller
- AuthController: register, login, login_guest, logout, change_password
- DashboardController: salam, tanggal, jam, jadwal_hari_ini, countdown_berikutnya, ringkasan_dzikir
- PrayerController: ambil_jadwal, simpan_preferensi, jadwal_offline, hitung_countdown
- QiblaController: hitung_bearing, arah_teks
- DzikirController: daftar_dzikir, simpan_tasbih, riwayat
- DoaController: daftar_kategori, daftar_doa, detail, toggle_favorit
- QuranController: daftar_surah, detail, toggle_favorit

## Service
- PrayerService: get_timings (API Aladhan)
- QiblaService: bearing_kiblat (perhitungan geografis ke Ka'bah)
- LocationService: GPS via Plyer
- NotificationService: notifikasi lokal via Plyer
- QuranService: daftar_surah (API equran.id)
- AudioService: pemutaran audio murottal

## View (KivyMD Screen)
SplashScreen, LoginScreen, RegisterScreen, DashboardScreen, PrayerScreen, QiblaScreen, DzikirScreen, DoaScreen, DoaDetailScreen, QuranScreen, SettingsScreen

## Relasi Antar-Kelas
User 1:N FavoriteDoa; User 1:N FavoriteSurah; User 1:N DzikirHistory
KategoriDoa 1:N Doa; Doa 1:N FavoriteDoa
Surah 1:N FavoriteSurah
Semua FK menggunakan ondelete="CASCADE".
