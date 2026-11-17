# SALATIFY — Dokumentasi Menjalankan & Deployment

## 1. Menjalankan Backend FastAPI (Lokal)

### Persyaratan
- Python 3.14+
- PostgreSQL (opsional untuk produksi; SQLite bisa untuk development)
- Library: `pip install -r backend/requirements.txt`

### Konfigurasi Database
Edit variabel environment atau file `.env`:

```bash
# Untuk PostgreSQL produksi:
export DATABASE_URL="postgresql+psycopg2://user:password@host:5432/salatify"

# Untuk SQLite development (default):
export DATABASE_URL="sqlite:///./salatify_web.db"
```

### Menjalankan Server
```bash
# Dari root proyek SALATIFY
cd backend
export SALATIFY_SECRET_KEY="ganti- dengan-kunci-rahasia-panjang"
export DATABASE_URL="sqlite:///./salatify_web.db"  # atau PostgreSQL URL
uvicorn main:app --host 127.0.0.1 --port 8000
```

### Mengakses API
- **Swagger Docs**: `http://127.0.0.1:8000/docs`
- **Health Check**: `http://127.0.0.1:8000/health`
- **Base URL**: `http://127.0.0.1:8000`

### Akun Default (Setelah Seed)
- Username: `hasan`, Email: `hasan@mail.com`, Password: `password123`
- Username: `luqman`, Email: `luqman@mail.com`, Password: `password123`
- Pengguna Tamu: Login via `/auth/guest`

### Migrasi Database (PostgreSQL)
Jika menggunakan PostgreSQL untuk pertambahan pengguna:
```bash
alembic upgrade head  # jika sudah diinisialisasi alembic
# Atau manually: Base.metadata.create_all(engine)
```

---

## 2. Menjalankan Website (HTML/CSS/JS)

### Persyaratan
- Backend FastAPI sudah berjalan (lihat bagian 1)
- Browser modern (Chrome, Edge, Firefox)

### Jalankan Website
Akses langsung melalui file HTML atau melalui backend:

```bash
# Cara 1: Buka file HTML langsung
open web/index.html

# Cara 2: Melalui backend FastAPI
# Backend sudah mount folder web di /
# Akses: http://127.0.0.1:8000/web/index.html
```

### Fitur Website
- **Landing Page**: `/web/index.html` - Menampilkan fitur utama SALATIFY
- **Login/Register**: `/web/login.html`, `/web/register.html`
- **Dashboard**: `/web/dashboard.html` - Melihat jadwal sholat, countdown, dzikir, doa, Qur'an, pengaturan
- **Jadwal Sholat**: `/web/prayer.html`
- **Arah Kiblat**: `/web/qibla.html`
- **Dzikir & Tasbih**: `/web/dzikir.html`
- **Kumpulan Doa**: `/web/doa.html` + detail `/web/doa-detail.html?id=1`
- **Al-Qur'an**: `/web/quran.html` - Daftar surah + pemutar audio placeholder
- **Pengaturan**: `/web/settings.html` - Tema, profil, password, pengingat, tentang

### Otentikasi
- Pengguna perlu login/register terlebih dahulu
- Token JWT disimpan di `localStorage`
- Setiap request API harus mengirim header: `Authorization: Bearer <token>`
- Jika token expired, akan diarahkan ke halaman login

### Service Worker (PWA)
Website mendukung Progressive Web App. Service worker `/sw.js` akan_cache asset utama untuk bekerja tanpa internet setelah kunjungan pertama.

---

## 3. Integrasi Aplikasi Android dengan Backend

### Adapter API (Opsional)
File: `services/api_client.py`

Adapter ini TAMBAHAN dan OPSIONAL. Aplikasi Android asli (KivyMD + SQLite) tetap berfungsi tanpa backend.

**Cara penggunaan di Android:**
```python
from services.api_client import SalatifyApiClient

client = SalatifyApiClient(base_url="http://10.0.2.2:8000")  # IP komputer di jaringan lokal

# Contoh: Login
data = client.login("hasan", "password123")
token = data["access_token"]

# Set token di localStorage Android (misalnya via SQLite atau file)
# Selanjutnya semua request akan otomatis menyertakan token

# Contoh: Daftar doa
doa_list = client.daftar_doa()

# Contoh: Jadwal sholat
jadwal = client.jadwal_hari_ini("-6.2", "106.8", "mwml")
```

**Catatan Penting:**
- Gunakan IP komputer host di jaringan lokal (biasanya `10.0.2.2` di Android emulator, atau IP WiFi di perangkat fisik)
- Pastikan firewall/security menyiurkan port 8000
- Jika tidak ada koneksi internet ke backend, aplikasi Android masih dapat bekerja secara lokal dengan SQLite
- Data yang disinkronkan: akun, favorit doa/surah, riwayat dzikir

### Buildozer APK (Linux/WSL2)
```bash
# Dari root proyek SALATIFY (di dalam WSL2 Ubuntu)
buildozer android debug
```
Lihat `buildozer.spec` untuk konfigurasi. APK hasil build akan ada di `bin/salatify-1.0.0-debug.apk`.

---

## 4. Deployment Website ke Production

### Opsi A: Render.com (Paling Mudah)
1. Buat repository Git (GitHub/GitLab)
2. Buat account di [render.com](https://render.com)
3. New Web Service → Connect Repository
4. Build Command: `pip install -r backend/requirements.txt`
5. Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Environment Variables: `DATABASE_URL`, `SALATIFY_SECRET_KEY`
7. Site akan tersedia di `https://salatify.onrender.com`

### Opsi B: Heroku
1. Buat `Procfile` di root: `web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
2. Tambah `requirements.txt` tambahan: `gunicorn`
3. `heroku create salatify`
4. `git push heroku main`
5. Set config vars: `DATABASE_URL`, `SALATIFY_SECRET_KEY`

### Opsi C: VPS (DigitalOcean, Vultr, dll)
1. VPS dengan Ubuntu 20.04/22.04
2. Install: `sudo apt install python3-pip python3-venv postgresql nginx`
3. Clone repo, `pip install -r backend/requirements.txt`
4. Setup Nginx sebagai reverse proxy ke uvicorn
5. Setup PostgreSQL dan migrasi
6. Setup SSL (Let's Encrypt via Certbot)

### Konfigurasi Produksi
- Gunakan `DATABASE_URL` PostgreSQL (tidak SQLite)
- Gunakan `SALATIFY_SECRET_KEY` yang kuat (minimal 32 karakter)
- Set `ALLOWED_HOSTs` di `backend/main.py` jika perlu
- Gunakan domain HTTPS (rekomendasi: `https://salatify.com`)
- Backup database rutin

---

## 5. Struktur Proyek Akhir

```
salatify/
├── main.py                  # Aplikasi Android KivyMD (asli)
├── main.kv                  # KV Language Android
├── requirements.txt         # Library Python Android
├── buildozer.spec           # Konfigurasi Buildozer APK
├── README.md                # Dokumentasi proyek utama
├── .gitignore

├── backend/               # FastAPI Shared Backend (BARU)
│   ├── main.py              # Aplikasi FastAPI
│   ├── models.py            # SQLAlchemy models (PostgreSQL/SQLite)
│   ├── database.py          # Engine & session
│   ├── seed.py              # Seeder data awal
│   ├── requirements.txt     # Library FastAPI
│   ├── auth.py              # JWT & password hashing
│   ├── routers/             # API routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── doa.py
│   │   ├── dzikir.py
│   │   ├── prayer.py
│   │   ├── qibla.py
│   │   ├── quran.py
│   │   └── reminder.py
│   ├── services/            # Layanan helper
│   │   ├── __init__.py
│   │   ├── prayer_service.py
│   │   └── qibla_service.py
│   ├── utils/               # Utility modul
│   │   ├── __init__.py
│   │   └── constants.py
│   └── api_client.py        # Android adapter (opsional)

├── web/                     # Website Frontend (BARU)
│   ├── index.html           # Landing page
│   ├── login.html           # Halaman login
│   ├── register.html        # Halaman daftar
│   ├── dashboard.html       # Halaman utama pengguna
│   ├── prayer.html          # Jadwal sholat
│   ├── qibla.html           # Kompas kiblat
│   ├── dzikir.html          # Dzikir & tasbih
│   ├── doa.html             # Kumpulan doa
│   ├── doa-detail.html      # Detail doa
│   ├── quran.html           # Al-Qur'an & murottal
│   ├── settings.html        # Pengaturan lengkap
│   ├── static/
│   │   ├── css/style.css    # Stylesheet konsisten dengan Android
│   │   └── js/
│   │       ├── api.js       # API client (JWT)
│   │       └── app.js       # UI helpers (toast, countdown, format)
│   ├── manifest.json        # PWA manifest
│   └── sw.js                # Service worker

├── docs/
│   ├── running_local.md     # Dokumentasi menjalankan lokal (ini file)
│   ├── deployment_guide.md  # Dokumentasi deployment produksi
│   ├── analisis_kebutuhan.md
│   ├── diagram_kelas.md
│   ├── relasi_database.md
│   └── panduan_penggunaan.md

└── services/                # Python services Android (asli)
    ├── __init__.py
    ├── api_client.py        # Adapter ke backend (opsional)
    ├── prayer_service.py
    ├── qibla_service.py
    └── ...
```

---

## 6. Versi Aplikasi

| Platform | Status | Versi |
|----------|--------|-------|
| Aplikasi Android (KivyMD) | ✅ Selesai & Diuji | 1.0.0 |
| Website Responsif | ✅ Selesai & Diuji | 1.0.0 |
| Backend API (FastAPI) | ✅ Berjalan | 1.0.0 |
| Database | ✅ SQLite (dev) / PostgreSQL (prod) | - |

---

**Catatan Penting:**
1. Aplikasi Android (KivyMD) sudah selesai dan berjalan secara lokal dengan SQLite. Backend FastAPI adalah fitur tambahan untuk sinkronisasi data ke website.
2. Website bersifat responsive dan dapat diakses dari browser apapun.
3. Data akun, favorit doa/surah, dan riwayat dzikir dapat sinkronisasi antara Android dan website melalui backend FastAPI.
4. Untuk deployment produksi, gunakan PostgreSQL dan HTTPS.
5. Lihat `buildozer.spec` untuk build APK di environment WSL2 Ubuntu.