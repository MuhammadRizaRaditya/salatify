# SALATIFY — Panduan Deployment Produksi

## Ringkas

| Langkah | Deskripsi |
|---------|-----------|
| 1. Repository | Push ke GitHub/GitLab |
| 2. Hosting | Pilih: Render.com (disarankan), Heroku, atau VPS |
| 3. PostgreSQL | Buat database, set `DATABASE_URL` |
| 4. Variabel Environment | `DATABASE_URL`, `SALATIFY_SECRET_KEY` (32+ karakter) |
| 5. Deploy | Set build & start commands di dashboard |
| 6. HTTPS | Otomatis via Let's Encrypt (Render/hered) |
| 7. Uji | Test semua 15 fitur via browser |

## Deploy ke Render.com (Direkomendasikan)

1. **Push kode ke GitHub**
   ```bash
   git init
   git add .
   git commit -m "SALATIFY full project"
   git remote add origin <repo-url>
   git push -u origin main
   ```

2. **Buat di Render.com**
   - Baru Web Service → Connect Repository
   - Root Directory: biarkan kosong (atau `backend/`)
   - Build Command: `cd backend && pip install -r requirements.txt` (atau `pip install -r backend/requirements.txt`)
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables:
     - `DATABASE_URL`: `postgresql+psycopg2://user:password@host:5432/salatify`
     - `SALATIFY_SECRET_KEY`: kunci rahasia panjang (misal: `sk_salatify_super_secret_32_chars_minimum`)

3. **Setelah Deploy**
   - Sitesi langsung hidup di `https://salatify.onrender.com`
- Buka `https://salatify.onrender.com/web/index.html` untuk website
- Buka `https://salatify.onrender.com/docs` untuk Swagger API docs

## Opsi: Heroku

1. Buat `Procfile` di root proyek:
   ```
   web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
2. Tambah `gunicorn` ke `backend/requirements.txt`:
   ```
   gunicorn==23.0.0
   ```
3. `heroku create salatify`
4. `git push heroku main`
5. Set config vars di Dashboard Heroku:
   - `DATABASE_URL`: URL koneksi PostgreSQL
   - `SALATIFY_SECRET_KEY`: rahasia panjang

## Opsi: VPS (DigitalOcean/Vultr)

1. VPS Ubuntu 20.04/22.04
2. `sudo apt update && sudo apt install python3-pip postgresql nginx -y`
3. `sudo -u postgres createuser -s salatify`
4. `sudo -u postgres createdb salatify`
5. Clone repo, `pip install -r backend/requirements.txt`
6. Setup Nginx reverse proxy ke uvicorn (port 8000)
7. `sudo certbot --nginx -d salatify.com` untuk HTTPS
8. Migrasi database jika perlu

## Catatan Penting Produksi

- **Gunakan PostgreSQL**, bukan SQLite untuk banyak pengguna
- **Gunakan HTTPS** dengan domain sendiri
- **Set SALATIFY_SECRET_KEY** yang kuat (minimal 32 karakter acak)
- **Backup database rutin** (harian/minimal mingguan)
- **Monitor penggunaan resource** (RAM/CPU di uvicorn)
- **Gunakan gunicorn** di atas production daripada direkt uvicorn
- **CORS** sudah di-set di `main.py` dengan `allow_origins=["*"]`—untuk production ganti dengan domain yang tepat

---

## Daftar Fitur yang Tersedia

### Aplikasi Android (KivyMD)
1. Splash Screen ✓
2. Login & Register ✓
3. Dashboard ✓
4. Jadwal Sholat ✓
5. Pengingat Sholat ✓
6. Arah Kiblat ✓
7. Wirid & Dzikir ✓
8. Kumpulan Doa (14 kategori) ✓
9. Al-Qur'an & Murottal ✓
10. Pengaturan ✓

### Website Responsif
1. Landing Page SALATIFY ✓
2. Register, Login, Logout, Guest Mode ✓
3. Dashboard pengguna ✓
4. Jadwal sholat berdasarkan lokasi ✓
5. Hitung mundur menuju sholat berikutnya ✓
6. Pengaturan pengingat sholat ✓
7. Arah kiblat ✓
8. Dzikir & tasbih digital ✓
9. Riwayat dzikir ✓
10. Kumpulan doa 14 kategori ✓
11. Pencarian & favorit doa ✓
12. Daftar 114 surah Al-Qur'an ✓
13. Pemutar audio murottal ✓
14. Pengaturan profil pengguna (tema, password, notifikasi) ✓
15. Tema terang & gelap ✓

---

**Total Fitur**: 15 fitur di website + 10 fitur di aplikasi Android (beberapa tumpang tindih, total unik > 15).

---

**Dikembangkan oleh**: Hasan, Luqman, Riza, dan Wisnu
**Versi**: 1.0.0
**Tahun**: 2026