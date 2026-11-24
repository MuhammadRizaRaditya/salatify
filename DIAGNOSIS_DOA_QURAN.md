# DIAGNOSIS: Halaman Doa & Al-Qur'an Tidak Menampilkan Data

## 1. Daftar Endpoint Backend

### Doa endpoints (backend/routers/doa.py):
- `GET /doa/kategori` — daftar kategori doa
- `GET /doa` — list doa (disesuaikan dengan query `?q=`)
- `GET /doa/{doa_id}` — detail doa
- `POST /doa/{doa_id}/favorit` — toggle favorit

### Quran/Surah endpoints (backend/routers/quran.py):
- `GET /quran/surah` — list surah (disesuaikan dengan query `?q=`)
- `GET /quran/surah/{surah_id}` — detail surah
- `POST /quran/surah/{surah_id}/favorit` — toggle favorit
- `GET /quran/api/surah` — endpoint alternatif (lihat quran.py:87)

### Penting: Di mana data diambil di website?

Dari `web/static/js/api.js`:
- `doa.list(q)` → `fetch(API_BASE + '/doa' + qs)` → backend FastAPI `/doa`
- `quran.list(q)` → `fetch(API_BASE + '/quran/surah' + qs)` → backend FastAPI `/quran/surah`

Jika backend tidak punya data, website akan menampilkan "Doa tidak ditemukan" atau "Surah tidak ditemukan".

## 2. Sumber Data: Website vs API equran.id

### web/static/js/api.js (doa & quran):
- Hanya memanggil **backend FastAPI** (`/doa` dan `/quran/surah`)
- **TIDAK** langsung ke `equran.id`
- Jika backend return `[]` atau error → halaman kosong

### services/quran_service.py:
- Menggunakan `equran.id/api/v2/surah` (publik, legal)
- Digunakan oleh Kivy service, bukan website langsung
- Fungsi: `daftar_surah()` → return `data["data"]` atau `None` jika gagal

### backend/seed.py:
- Data seed hanya 10 surah (no 1 through 10)
- Jumlah doa: 37 dalam 12 kategori
- Jumlah dzikir: 8 dalam 4 kategori
- Fungsi `run_seed()` hanya dieksekusi jika `python backend/seed.py` dijalankan secara manual

## 3. Isi Database Saat Ini

Database `backend/database.db` ada tapi **KOSONG** (0 tabel):
- Tidak ada tabel `surah`, `kategori_doa`, `doa`
- Seeder pernah dijalankan atau tidak, tabel tidak tercipta
- Akibatnya, endpoint `/doa` dan `/quran/surah` mengembalikan data kosong

## 4. Aplikasi Kivy: Database & Seeder

### database/seeder (di dalam `backend/seed.py`):
- `SURAH_SEED` hanya berisi 10 surah (1-10)
- Jika `equran.id` tidak bisa diakses → `QuranService.daftar_surah()` return `None`
- Aplikasi Kivy akan menampilkan surah yang sudah di-seed (hanya 10) atau kosong jika belum di-seed

### main.py (Kivy entry point):
- Memanggil `init_db(self.app_data_dir)` untuk membuat database SQLite
- **TIDAK** otomatis memanggil `run_seed()` seeding
- `main.kv` hanya 40 bytes — hanya struktur UI minimal, tidak berisi logika data

### Kondisi Kivy:
- Jika `equran.id` bisa diakses di waktu build: 10 surah pertama saja yang tersimpan
- Jika `equran.id` gagal: database kosong, surah tidak tampil sama sekali
- Tidak ada fallback ke API publik di dalam kode Kivy

## 5. Analisis Keseluruhan Masalah

### Kasus Website (kosong):
1. **Root cause**: Database backend kosong (0 tabel)
2. **Aliran**: Browser → `/doa` → `GET /doa` → query DB → return `[]` → `doa.html` menampilkan "Doa tidak ditemukan"
3. **Sama untuk**: `/quran/surah` → return `[]` → `quran.html` menampilkan "Surah tidak ditemukan"

### Kasus Kivy (kosong):
1. **Root cause**: Database Kivy tidak memiliki tabel data (tidak ada seeder yang dijalankan)
2. **Aliran**: Aplikasi Kivy → `init_db()` → tabel kosong → `QuranService.daftar_surah()` → coba `equran.id` → bisa gagal (timeout/jaringan) → return `None` → surah tidak tampil
3. **Faktor kedua**: `SURAH_SEED` hanya 10 surah, jika equran.id gagal hanya 10 surah yang akan tampil (jika sebelumnya berhasil di-seed)

## 6. Perbaikan Terkecil & Rekomendasi

### Website — paling kecil:
1. **Seed database**: Jalankan `python backend/seed.py` (atau `python -m backend.seed`)
2. Atau: Ubah `web/static/js/api.js` untuk fallback langsung ke `equran.id` jika backend gagal:
   - Ubah `doa.list()` dan `quran.list()` untuk memiliki backup API
   - *Catatan*: Ini menghapus dependensi ke backend untuk data dinamis

### Kivy — paling kecil:
1. **Jalankan seeder setelah init_db**: Di `main.py`, setelah `init_db()`, tambahkan:
   ```python
   from backend.seed import run_seed
   run_seed()
   ```
2. Atau: Tambahkan fallback di `services/quran_service.py` jika `equran.id` gagal

### Solusi menyeluruh (arahan):
1. **Jalankan seeder sekali**: `python backend/seed.py` → isi tabel SQLite di backend dan di Kivy
2. **Verifikasi endpoint**: Pastikan `python -m unittest discover -s tests` lulus setelah seed
3. **Tambahkan fallback di website**: Ubah `api.js` agar bisa fallback ke `equran.id` jika backend `/doa`/`/quran/surah` kosong
4. **Perbaiki Kivy seeding**: Tambahkan `run_seed()` dipelopori di `main.py` setelah `init_db()`
5. **Perbaiki SURAH_SEED**: Tambahkan surah 11-114 jika butuh lengkap (sekarang hanya 1-10)

### Laporan Periode:
- **Sebab**: Database backend & Kivy kosong, seeder belum pernah dijalankan atau gagal
- **Buktikan**: `python check_db2.py` menampilkan 0 tabel di database
- **Perbaikan**: Jalankan `python backend/seed.py` dan verifikasi data muncul di `/doa` dan `/quran/surah` endpoint