# Relasi Database

Database SQLite dikelola oleh SQLAlchemy ORM, file berada di `app_user_data_dir` (Android) atau direktori pengguna (desktop).

## Tabel dan Kolom Utama

| Tabel | Primary Key | Foreign Key | Keterangan |
|---|---|---|---|
| users | id | — | Akun pengguna |
| kategori_doa | id | — | Kategori doa |
| doa | id | kategori_id → kategori_doa.id | Isi doa |
| favorite_doa | id | user_id → users.id; doa_id → doa.id | Doa favorit per user |
| dzikir | id | — | Kumpulan dzikir |
| dzikir_history | id | user_id → users.id | Riwayat tasbih per user |
| jadwal_sholat | id | — | Jadwal sholat harian |
| prayer_preferences | id | — | Preferensi lokasi & metode |
| user_settings | id | — | Pengaturan pengguna |
| surah | id | — | Data surah Al-Qur'an |
| favorite_surah | id | user_id → users.id; surah_id → surah.id | Surah favorit per user |

## Integritas Referensial
- Semua foreign key menggunakan `ON DELETE CASCADE`.
- Primary key berupa integer auto-increment.
- Username dan email unik (unique constraint, index).
- Seeder idempoten: memeriksa keberadaan data sebelum insert, tidak ada duplikasi saat dijalankan berulang.

## Pengelolaan Transaksi
- Setiap operasi write menggunakan `session.commit()`.
- Error database ditangani dengan try/except pada controller.
