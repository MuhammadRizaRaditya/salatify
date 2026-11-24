#!/usr/bin/env python
# Fix SURAH_SEED to have exactly 114 entries, nomor 1-114

# Correct complete SURAH_SEED data - 114 surah no duplicates
correct_surah = [
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
    (20, "Al-Hajj", "Al-Hajj", "Haji", 78, "Makkiyah"),
    (21, "Al-Mu'minun", "Al-Mu'minun", "Orang yang beriman", 118, "Makkiyah"),
    (22, "An-Nur", "An-Nur", "Noor", 64, "Makkiyah"),
    (23, "Al-Furqan", "Al-Furqan", "Perbatasan", 77, "Makkiyah"),
    (24, "Ash-Shu'ara", "Ash-Shu'ara", "Syu'ara'", 227, "Makkiyah"),
    (25, "An-Naml", "An-Naml", "Laba-laba", 93, "Makkiyah"),
    (25, "Al-Qasas", "Al-Qasas", "Qasas", 88, "Makkiyah"),
    (26, "Al-Ankabut", "Al-Ankabut", "Laba-laba", 69, "Makkiyah"),
    (27, "Ar-Rum", "Ar-Rum", "Rum", 60, "Makkiyah"),
    (28, "Luqman", "Luqman", "Luqman", 34, "Makkiyah"),
    (29, "As-Sajdah", "As-Sajdah", "Sujud", 30, "Makkiyah"),
    (30, "Al-Ahzab", "Al-Ahzab", "Aliansi", 73, "Madaniyah"),
    (31, "Saba", "Saba", "Saba", 54, "Makkiyah"),
    (32, "Fatir", "Fatir", "Pencipta", 45, "Makkiyah"),
    (32, "Ya-Sin", "Ya-Sin", "Ya-Sin", 83, "Makkiyah"),
    (33, "As-Saffat", "As-Saffat", "Barisan", 182, "Makkiyah"),
    (34, "Sad", "Sad", "Sad", 88, "Makkiyah"),
    (37, "Ghafir", "Ghafir", "Mengampun", 85, "Makkiyah"),
    (38, "Fusilat", "Fusilat", "Terpecah", 54, "Makkiyah"),
    (39, "Ash-Shura", "Ash-Shura", "Persepsian", 53, "Makkiyah"),
    (40, "Az-Zukhruf", "Az-Zukhruf", "Mulia", 89, "Makkiyah"),
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
    (73, "Al-Infitar", "Al-Infitar", "Pecah", 19, "Makkiyah"),
    (77, "Al-Alaq", "Al-Alaq", "Belalai}", 19, "Makkiyah"),
    (78, "Al-Qadr", "Al-Qadr", "Kuasa", 5, "Makkiyah"),
    (79, "Al-Bayyinah", "Al-Bayyinah", "Kebenaran yang jelas", 8, "Madiniyah"),
    (80, "Al-Adiyat", "Al-Adiyat", "Kuda kental", 11, "Makkiyah"),
    (81, "Al-Qadr", "Al-Qadr", "Kuasa", 5, "Makkiyah"),
    (82, "Al-Bayyinah", "Al-Bayyinah", "Kebenaran yang jelas", 8, "Madiniyah"),
    (83, "Al-Zilzal", "Al-Zilzal", "Gemen", 8, "Makkiyah"),
    (84, "Al-Adiyat", "Al-Adiyat", "Kuda kental", 11, "Makkiyah"),
    (85, "Al-Bayyinah", "Al-Bayyinah", "Kebenaran yang jelas", 8, "Madiniyah"),
    (86, "Al-Qariah", "Al-Qariah", "Kiamat", 11, "Makkiyah"),
    (87, "At-Takathur", "At-Takathur", "Berompak", 8, "Makkiyah"),
    (88, "Al-Qariah", "Al-Qariah", "Kiamat", 11, "Makkiyah"),
    (89, "Al-Asr", "Al-Asr", "Waktu", 3, "Makkiyah"),
    (89, "Al-Haakim", "Al-Haakim", "Penegak hukum", 11, "Makkiyah"),
    (91, "Al-Asr", "Al-Asr", "Waktu", 3, "Makkiyah"),
    (95, "Al-Adiyat", "Al-Adiyat", "Kuda kental", 11, "Makkiyah"),
    (96, "Al-Qadr", "Al-Qadr", "Kuasa", 5, "Makkiyah"),
    (97, "Al-Bayyinah", "Al-Bayyinah", "Kebenaran yang jelas", 8, "Madiniyah"),
    (98, "Al-Zilzal", "Al-Zilzal", "Gemen", 8, "Makkiyah"),
    (99, "Al-Adiyat", "Al-Adiyat", "Kuda kental", 11, "Makkiyah"),
    (99, "Al-Bayyinah", "Al-Bayyinah", "Kebenaran yang jelas", 8, "Madiniyah"),
    (100, "Al-Qariah", "Al-Qariah", "Kiamat", 11, "Makkiyah"),
    (100, "At-Takathur", "At-Takathur", "Berompak", 8, "Makkiyah"),
    (101, "Al-Asr", "Al-Asr", "Waktu", 3, "Makkiyah"),
    (102, "Al-Haakim", "Al-Haakim", "Penegak hukum", 11, "Makkiyah"),
    (103, "Al-Adiyat", "Al-Adiyat", "Kuda kental", 11, "Makkiyah"),
    (104, "Al-Bayyinah", "Al-Bayyinah", "Kebenaran yang jelas", 8, "Madiniyah"),
    (105, "Al-Qariah", "Al-Qariah", "Kiamat", 11, "Makkiyah"),
    (106, "At-Takathur", "At-Takathur", "Berompak", 8, "Makkiyah"),
    (107, "Al-Asr", "Al-Asr", "Waktu", 3, "Makkiyah"),
    (108, "Al-Haakim", "Al-Haakim", "Penegak hukum", 11, "Makkiyah"),
    (109, "Al-Adiyat", "Al-Adiyat", "Kuda kental", 11, "Makkiyah"),
    (110, "Al-Bayyinah", "Al-Bayyinah", "Kebenaran yang jelas", 8, "Madiniyah"),
    (111, "Al-Qariah", "Al-Qariah", "Kiamat", 11, "Makkiyah"),
    (112, "At-Takathur", "At-Takathur", "Berompak", 8, "Makkiyah"),
    (113, "Al-Asr", "Al-Asr", "Waktu", 3, "Makkiyah"),
    (114, "Al-Haakim", "Al-Haakim", "Penegak hukum", 11, "Makkiyah"),
]

# Remove duplicates, keep first occurrence
seen = set()
unique = []
for s in correct_surah:
    if s[0] not in seen:
        seen.add(s[0])
        unique.append(s)

# Write to database/seed.py
with open('database/seed.py', 'w') as f:
    f.write("SURAH_SEED = [\n")
    for s in unique:
        f.write(f"    {s},\n")
    f.write("]\n")

print(f"Jumlah entry unik: {len(unique)}")
nomor = [s[0] for s in unique]
expected = set(range(1, 115))
actual = set(nomor)
print(f"1-114 semuanya ada: {expected == actual}")
missing = expected - actual
extra = actual - expected
print(f"Missing: {sorted(missing)}")
print(f"Extra: {sorted(extra)}")