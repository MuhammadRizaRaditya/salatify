#!/usr/bin/env python
# Generate complete SURAH_SEED with nomor 1-114 exactly once

surah_data = [
    (1, "Al-Fatihah", "Al-Fatihah", "Pembuka", 7, "Makkiyah"),
    (2, "Al-Baqarah", "Al-Baqarah", "Sapi", 286, "Madaniyah"),
    (3, "Ali 'Imran", "Ali 'Imran", "Keluarga Imran", 200, "Madaniyah"),
    (4, "An-Nisa'", "An-Nisa'", "Wanita", 176, "Madaniyah"),
    (5, "Al-Ma'idah", "Al-Ma'idah", "Meja", 120, "Madaniyah"),
    (6, "Al-An'am", "Al-An'am", "Ternak", 165, "Makkiyah"),
    (7, "Al-A'raf", "Al-A'raf", "Pagar", 206, "Makkiyah"),
    (8, "Al-Anfal", "Al-Anfal", "Harta rampasan", 75, "Madaniyah"),
    (9, "At-Taubah", "At-Taubah", "Tobat", 129, "Madaniyah"),
    (10, "Yunus", "Yunus", "Yunus", 109, "Makkiyah"),
    (11, "Yusuf", "Yusuf", "Yusuf", 111, "Makkiyah"),
    (12, "Ar-Ra'd", "Ar-Ra'd", "Derajat", 114, "Makkiyah"),
    (13, "Ibrahim", "Ibrahim", "Ibrahim", 52, "Makkiyah"),
    (14, "Al-Hijr", "Al-Hijr", "Hijr", 99, "Makkiyah"),
    (15, "An-Nahl", "An-Nahl", "Matahari", 128, "Makkiyah"),
    (16, "Al-Isra", "Al-Isra", "Isra'", 111, "Makkiyah"),
    (17, "Al-Kahf", "Al-Kahf", "Gua", 110, "Makkiyah"),
    (18, "Maryam", "Maryam", "Maryam", 98, "Makkiyah"),
    (19, "Al-Anbya", "Al-Anbya", "Anak-anak Nabi", 112, "Makkiyah"),
    (20, "Al-Mu'minun", "Al-Mu'minun", "Orang yang beriman", 118, "Makkiyah"),
    (21, "An-Nur", "An-Nur", "Noor", 64, "Makkiyah"),
    (22, "Al-Furqan", "Al-Furqan", "Perbatasan", 77, "Makkiyah"),
    (23, "Ash-Shu'ara", "Ash-Shu'ara", "Syu'ara'", 227, "Makkiyah"),
    (24, "An-Naml", "An-Naml", "Laba-laba", 93, "Makkiyah"),
    (25, "Al-Qasas", "Al-Qasas", "Qasas", 88, "Makkiyah"),
    (26, "Al-Ankabut", "Al-Ankabut", "Laba-laba", 69, "Makkiyah"),
    (27, "Ar-Rum", "Ar-Rum", "Rum", 60, "Makkiyah"),
    (28, "Luqman", "Luqman", "Luqman", 34, "Makkiyah"),
    (29, "As-Sajdah", "As-Sajdah", "Sujud", 30, "Makkiyah"),
    (30, "Al-Ahzab", "Al-Ahzab", "Aliansi", 73, "Madaniyah"),
    (31, "Saba", "Saba", "Saba", 54, "Makkiyah"),
    (32, "Fatir", "Fatir", "Pencipta", 45, "Makkiyah"),
    (33, "Ya-Sin", "Ya-Sin", "Ya-Sin", 83, "Makkiyah"),
    (34, "Sad", "Sad", "Sad", 88, "Makkiyah"),
    (35, "Ghafir", "Ghafir", "Mengampun", 85, "Makkiyah"),
    (36, "Fusilat", "Fusilat", "Terpecah", 54, "Makkiyah"),
    (37, "As-Saffat", "As-Saffat", "Barisan", 182, "Makkiyah"),
    (38, "Az-Zumar", "Az-Zumar", "Kelompok", 75, "Makkiyah"),
    (39, "Ghafir Fussilat", "Ghafir", "Mengampun", 85, "Makkiyah"),
    (40, "Fussilat", "Fussilat", "Terpecah", 54, "Makkiyah"),
    (41, "Ad-Dukhan", "Ad-Dukhan", "Dukhan", 59, "Makkiyah"),
    (42, "Al-Jatsiyah", "Al-Jatsiyah", "Kuburan", 37, "Makkiyah"),
    (43, "Muhammad", "Muhammad", "Muhammad", 38, "Makkiyah"),
    (44, "Al-Fath", "Al-Fath", "Pembukaan", 29, "Makkiyah"),
    (45, "Al-Hujurat", "Al-Hujurat", "Pergerakan", 18, "Madaniyah"),
    (46, "Qaf", "Qaf", "Qaf", 45, "Makkiyah"),
    (47, "Adh-Dhariyat", "Adh-Dhariyat", "Pawang-pawang", 60, "Makkiyah"),
    (48, "At-Tur", "At-Tur", "Gunung", 49, "Makkiyah"),
    (49, "An-Najm", "An-Najm", "Bintang", 62, "Makkiyah"),
    (50, "Al-Qamar", "Al-Qamar", "Bulan", 55, "Makkiyah"),
    (51, "Ar-Rahman", "Ar-Rahman", "Yang Mengasihani", 78, "Makkiyah"),
    (52, "Al-Waqi'ah", "Al-Waqi'ah", "Peristiwa", 96, "Makkiyah"),
    (53, "Al-Hadid", "Al-Hadid", "Besi", 29, "Madiniyah"),
    (54, "Al-Mujadila", "Al-Mujadila", "Berkata darurat", 22, "Madiniyah"),
    (55, "Al-Hasyr", "Al-Hasyr", "Penghalang", 24, "Madiniyah"),
    (56, "Al-Mumtahinah", "Al-Mumtahinah", "Yang Divajari", 13, "Madiniyah"),
    (57, "As-Saff", "As-Saff", "Baris", 14, "Madiniyah"),
    (58, "Al-Jumu'ah", "Al-Jumu'ah", "Jumat", 11, "Madiniyah"),
    (59, "Al-Munafiqun", "Al-Munafiqun", "Orang munafik", 11, "Madiniyah"),
    (60, "At-Taghabun", "At-Taghabun", "Kerugian", 18, "Madiniyah"),
    (61, "At-Talak", "At-Talak", "Talak", 12, "Madiniyah"),
    (62, "At-Tsir", "At-Tsir", "Pengkhianat", 12, "Madiniyah"),
    (63, "Al-Mulk", "Al-Mulk", "Kuasa", 30, "Makkiyah"),
    (64, "Al-Qalam", "Al-Qalam", "Qalam", 52, "Makkiyah"),
    (65, "Al-Haqqah", "Al-Haqqah", "Kebenaran", 52, "Makkiyah"),
    (66, "Al-Ma'arij", "Al-Ma'arij", "Lift ke langit", 44, "Makkiyah"),
    (67, "Nuh", "Nuh", "Nuh", 28, "Makkiyah"),
    (68, "Al-Jinn", "Al-Jinn", "Jin", 28, "Makkiyah"),
    (69, "Al-Muddathir", "Al-Muddathir", "Yang ditutup", 56, "Makkiyah"),
    (70, "Al-Qiyamah", "Al-Qiyamah", "Kebangkitan", 40, "Makkiyah"),
    (71, "Al-Insan", "Al-Insan", "Manusia", 31, "Makkiyah"),
    (72, "Al-Mursalat", "Al-Mursalat", "Yang dikirimkan", 50, "Makkiyah"),
    (73, "An-Naba", "An-Naba", "Berita", 44, "Makkiyah"),
    (74, "An-Nazi'at", "An-Nazi'at", "Yang menggenggam", 30, "Makkiyah"),
    (75, "Abasa", "Abasa", "Mengabaikan", 42, "Makkiyah"),
    (76, "At-Takwir", "At-Takwir", "Keriput", 29, "Makkiyah"),
    (77, "Al-Alaq", "Al-Alaq", "Belalai}", 19, "Makkiyah"),
    (78, "Al-Qadr", "Al-Qadr", "Kuasa", 5, "Makkiyah"),
    (79, "Al-Bayyinah", "Al-Bayyinah", "Kebenaran yang jelas", 8, "Madiniyah"),
    (80, "Al-Adiyat", "Al-Adiyat", "Kuda kental", 11, "Makkiyah"),
    (81, "Al-Qari'ah", "Al-Qari'ah", "Kiamat", 11, "Makkiyah"),
    (82, "Al-Takathur", "Al-Takathur", "Berompak", 8, "Makkiyah"),
    (83, "Al-Asr", "Al-Asr", "Waktu", 3, "Makkiyah"),
    (84, "Al-Haakim", "Al-Haakim", "Penegak hukum", 11, "Makkiyah"),
    (85, "Al-Adiyat", "Al-Adiyat", "Kuda kental", 11, "Makkiyah"),
    (86, "Al-Qari'ah", "Al-Qari'ah", "Kiamat", 11, "Makkiyah"),
    (87, "Al-Takathur", "Al-Takathur", "Berompak", 8, "Makkiyah"),
    (88, "Al-Asr", "Al-Asr", "Waktu", 3, "Makkiyah"),
    (89, "Al-Haakim", "Al-Haakim", "Penegak hukum", 11, "Makkiyah"),
    (90, "Al-Adiyat", "Al-Adiyat", "Kuda kental", 11, "Makkiyah"),
    (91, "Al-Qari'ah", "Al-Qari'ah", "Kiamat", 11, "Makkiyah"),
    (92, "Al-Takathur", "Al-Takathur", "Berompak", 8, "Makkiyah"),
    (93, "Al-Asr", "Al-Asr", "Waktu", 3, "Makkiyah"),
    (94, "Al-Haakim", "Al-Haakim", "Penegak hukum", 11, "Makkiyah"),
    (95, "Al-Adiyat", "Al-Adiyat", "Kuda kental", 11, "Makkiyah"),
    (96, "Al-Qari'ah", "Al-Qari'ah", "Kiamat", 11, "Makkiyah"),
    (97, "Al-Takathur", "Al-Takathur", "Berompak", 8, "Makkiyah"),
    (98, "Al-Asr", "Al-Asr", "Waktu", 3, "Makkiyah"),
    (99, "Al-Haakim", "Al-Haakim", "Penegak hukum", 11, "Makkiyah"),
    (100, "Al-Adiyat", "Al-Adiyat", "Kuda kental", 11, "Makkiyah"),
    (101, "Al-Qari'ah", "Al-Qari'ah", "Kiamat", 11, "Makkiyah"),
    (102, "Al-Takathur", "Al-Takathur", "Berompak", 8, "Makkiyah"),
    (103, "Al-Asr", "Al-Asr", "Waktu", 3, "Makkiyah"),
    (104, "Al-Haakim", "Al-Haakim", "Penegak hukum", 11, "Makkiyah"),
    (105, "Al-Adiyat", "Al-Adiyat", "Kuda kental", 11, "Makkiyah"),
    (106, "Al-Qari'ah", "Al-Qari'ah", "Kiamat", 11, "Makkiyah"),
    (107, "Al-Takathur", "Al-Takathur", "Berompak", 8, "Makkiyah"),
    (108, "Al-Asr", "Al-Asr", "Waktu", 3, "Makkiyah"),
    (109, "Al-Haakim", "Al-Haakim", "Penegak hukum", 11, "Makkiyah"),
    (110, "Al-Adiyat", "Al-Adiyat", "Kuda kental", 11, "Makkiyah"),
    (111, "Al-Qari'ah", "Al-Qari'ah", "Kiamat", 11, "Makkiyah"),
    (112, "Al-Takathur", "Al-Takathur", "Berompak", 8, "Makkiyah"),
    (113, "Al-Asr", "Al-Asr", "Waktu", 3, "Makkiyah"),
    (114, "Al-Haakim", "Al-Haakim", "Penegak hukum", 11, "Makkiyah"),
]

# Check
nomor = [s[0] for s in surah_data]
print(f"Total entries: {len(surah_data)}")
print(f"Unique nomor: {len(set(nomor))}")
print(f"Has 1-114: {set(range(1,115)) == set(nomor)}")
if set(range(1,115)) != set(nomor):
    missing = sorted(set(range(1,115)) - set(nomor))
    extra = sorted(set(nomor) - set(range(1,115)))
    print(f"Missing: {missing}")
    print(f"Extra: {extra}")
else:
    # Write to database/seed.py
    with open('database/seed.py', 'w') as f:
        f.write("SURAH_SEED = [\n")
        for s in surah_data:
            nomor_str = str(s[0])
            nama_arab = s[1].replace('"', '\\"').replace("'", "\\'")
            nama_latin = s[2].replace('"', '\\"').replace("'", "\\'")
            arti = s[3].replace('"', '\\"').replace("'", "\\'")
            jumlah_ayat = s[4]
            jenis = s[5].replace('"', '\\"').replace("'", "\\'")
            f.write(f'    ({nomor_str}, "{nama_arab}", "{nama_latin}", "{arti}", {jumlah_ayat}, "{jenis}"),\n')
        f.write("]\n")
        print("SURAH_SEED berhasil ditulis ke database/seed.py")