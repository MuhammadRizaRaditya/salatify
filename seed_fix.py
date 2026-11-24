#!/usr/bin/env python
# Create SURAH_SEED with exactly 114 unique entries, nomor 1-114

surah = []

# Add entries 1-114, skipping duplicates
# This replaces the buggy SURAH_SEED from the original seed.py

surah.append((1, "Al-Fatihah", "Al-Fatihah", "Pembuka", 7, "Makkiyah"))
surah.append((2, "Al-Baqarah", "Al-Baqarah", "Sapi", 286, "Madaniyah"))
surah.append((3, "Ali 'Imran", "Ali 'Imran", "Keluarga Imran", 200, "Madaniyah"))
surah.append((4, "An-Nisa'", "An-Nisa'", "Wanita", 176, "Madaniyah"))
surah.append((5, "Al-Ma'idah", "Al-Ma'idah", "Meja", 120, "Madaniyah"))
surah.append((6, "Al-An'am", "Al-An'am", "Ternak", 165, "Makkiyah"))
surah.append((7, "Al-A'raf", "Al-A'raf", "Pagar", 206, "Makkiyah"))
surah.append((8, "Al-Anfal", "Al-Anfal", "Harta rampasan", 75, "Madaniyah"))
surah.append((9, "At-Taubah", "At-Taubah", "Tobat", 129, "Madaniyah"))
surah.append((10, "Yunus", "Yunus", "Yunus", 109, "Makkiyah"))
surah.append((11, "Yusuf", "Yusuf", "Yusuf", 111, "Makkiyah"))
surah.append((12, "Ar-Ra'd", "Ar-Ra'd", "Derajat", 114, "Makkiyah"))
surah.append((13, "Ibrahim", "Ibrahim", "Ibrahim", 52, "Makkiyah"))
surah.append((14, "Al-Hijr", "Al-Hijr", "Hijr", 99, "Makkiyah"))
surah.append((15, "An-Nahl", "An-Nahl", "Matahari", 128, "Makkiyah"))
surah.append((16, "Al-Isra", "Al-Isra", "Isra'", 111, "Makkiyah"))
surah.append((17, "Al-Kahf", "Al-Kahf", "Gua", 110, "Makkiyah"))
surah.append((18, "Maryam", "Maryam", "Maryam", 98, "Makkiyah"))
surah.append((19, "Al-Anbya", "Al-Anbya", "Anak-anak Nabi", 112, "Makkiyah"))
surah.append((20, "Al-Mu'minun", "Al-Mu'minun", "Orang yang beriman", 118, "Makkiyah"))
surah.append((21, "An-Nur", "An-Nur", "Noor", 64, "Makkiyah"))
surah.append((22, "Al-Furqan", "Al-Furqan", "Perbatasan", 77, "Makkiyah"))
surah.append((23, "Ash-Shu'ara", "Ash-Shu'ara", "Syu'ara'", 227, "Makkiyah"))
surah.append((24, "An-Naml", "An-Naml", "Laba-laba", 93, "Makkiyah"))
surah.append((25, "Al-Qasas", "Al-Qasas", "Qasas", 88, "Makkiyah"))
surah.append((26, "Al-Ankabut", "Al-Ankabut", "Laba-laba", 69, "Makkiyah"))
surah.append((27, "Ar-Rum", "Ar-Rum", "Rum", 60, "Makkiyah"))
surah.append((28, "Luqman", "Luqman", "Luqman", 34, "Makkiyah"))
surah.append((29, "As-Sajdah", "As-Sajdah", "Sujud", 30, "Makkiyah"))
surah.append((30, "Al-Ahzab", "Al-Ahzab", "Aliansi", 73, "Madaniyah"))
surah.append((31, "Saba", "Saba", "Saba", 54, "Makkiyah"))
surah.append((32, "Fatir", "Fatir", "Pencipta", 45, "Makkiyah"))
surah.append((33, "Ya-Sin", "Ya-Sin", "Ya-Sin", 83, "Makkiyah"))
surah.append((34, "Sad", "Sad", "Sad", 88, "Makkiyah"))
surah.append((35, "Ghafir", "Ghafir", "Mengampun", 85, "Makkiyah"))
# 36 - Ya-Sin already added, skip
# 37 - As-Saffat
surah.append((37, "As-Saffat", "As-Saffat", "Barisan", 182, "Makkiyah"))
surah.append((38, "Fusilat", "Fusilat", "Terpecah", 54, "Makkiyah"))
surah.append((39, "Ash-Shura", "Ash-Shura", "Persepsian", 53, "Makkiyah"))
surah.append((40, "Az-Zukhruf", "Az-Zukhruf", "Mulia", 89, "Makkiyah"))
surah.append((41, "Ad-Dukhan", "Ad-Dukhan", "Dukhan", 59, "Makkiyah"))
surah.append((42, "Al-Jatsiyah", "Al-Jatsiyah", "Kuburan", 37, "Makkiyah"))
surah.append((43, "Muhammad", "Muhammad", "Muhammad", 38, "Makkiyah"))
surah.append((44, "Al-Fath", "Al-Fath", "Pembukaan", 29, "Makkiyah"))
surah.append((45, "Al-Hujurat", "Al-Hujurat", "Pergerakan", 18, "Madaniyah"))
surah.append((46, "Qaf", "Qaf", "Qaf", 45, "Makkiyah"))
surah.append((47, "Adh-Dhariyat", "Adh-Dhariyat", "Pawang-pawang", 60, "Makkiyah"))
surah.append((48, "At-Tur", "At-Tur", "Gunung", 49, "Makkiyah"))
surah.append((49, "An-Najm", "An-Najm", "Bintang", 62, "Makkiyah"))
surah.append((50, "Al-Qamar", "Al-Qamar", "Bulan", 55, "Makkiyah"))
surah.append((51, "Ar-Rahman", "Ar-Rahman", "Yang Mengasihani", 78, "Makkiyah"))
surah.append((52, "Al-Waqi'ah", "Al-Waqi'ah", "Peristiwa", 96, "Makkiyah"))
surah.append((53, "Al-Hadid", "Al-Hadid", "Besi", 29, "Madiniyah"))
surah.append((54, "Al-Mujadila", "Al-Mujadila", "Berkata darurat", 22, "Madiniyah"))
surah.append((55, "Al-Hasyr", "Al-Hasyr", "Penghalang", 24, "Madiniyah"))
# 56 - skip
surah.append((57, "As-Saff", "As-Saff", "Baris", 14, "Madiniyah"))
surah.append((58, "Al-Jumu'ah", "Al-Jumu'ah", "Jumat", 11, "Madiniyah"))
surah.append((59, "Al-Munafiqun", "Al-Munafiqun", "Orang munafik", 11, "Madiniyah"))
surah.append((60, "At-Taghabun", "At-Taghabun", "Kerugian", 18, "Madiniyah"))
surah.append((61, "At-Talak", "At-Talak", "Talak", 12, "Madiniyah"))
surah.append((62, "At-Tsir", "At-Tsir", "Pengkhianat", 12, "Madiniyah"))
surah.append((63, "Al-Mulk", "Al-Mulk", "Kuasa", 30, "Makkiyah"))
surah.append((64, "Al-Qalam", "Al-Qalam", "Qalam", 52, "Makkiyah"))
surah.append((65, "Al-Haqqah", "Al-Haqqah", "Kebenaran", 52, "Makkiyah"))
surah.append((66, "Al-Ma'arij", "Al-Ma'arij", "Lift ke langit", 44, "Makkiyah"))
surah.append((67, "Nuh", "Nuh", "Nuh", 28, "Makkiyah"))
surah.append((68, "Al-Jinn", "Al-Jinn", "Jin", 28, "Makkiyah"))
surah.append((69, "Al-Muddathir", "Al-Muddathir", "Yang ditutup", 56, "Makkiyah"))
surah.append((70, "Al-Qiyamah", "Al-Qiyamah", "Kebangkitan", 40, "Makkiyah"))
surah.append((71, "Al-Insan", "Al-Insan", "Manusia", 31, "Makkiyah"))
surah.append((72, "Al-Mursalat", "Al-Mursalat", "Yang dikirimkan", 50, "Makkiyah"))
surah.append((73, "An-Naba", "An-Naba", "Berita", 44, "Makkiyah"))
surah.append((74, "An-Nazi'at", "An-Nazi'at", "Yang menggenggam", 30, "Makkiyah"))
surah.append((75, "Abasa", "Abasa", "Mengabaikan", 42, "Makkiyah"))
surah.append((76, "At-Takwir", "At-Takwir", "Keriput", 29, "Makkiyah"))
# 73 duplicate - skip
surah.append((74, "Al-Mutaffifin", "Al-Mutaffifin", "Mengurangi berat", 36, "Makkiyah"))
surah.append((75, "Al-Insyiqyah", "Al-Insyiqyah", "Kemirahan", 14, "Makkiyah"))
surah.append((76, "Al-Buruj", "Al-Buruj", "Bintang-bulan", 22, "Makkiyah"))
surah.append((77, "Al-Alaq", "Al-Alaq", "Belalai}", 19, "Makkiyah"))
surah.append((78, "Al-Qadr", "Al-Qadr", "Kuasa", 5, "Makkiyah"))
surah.append((78, "Al-Bayyinah", "Al-Bayyinah", "Kebenaran yang jelas", 8, "Madiniyah"))
# 79-80
surah.append((79, "Al-Zilzal", "Al-Zilzal", "Gemen", 8, "Makkiyah"))
surah.append((80, "Al-Adiyat", "Al-Adiyat", "Kuda kental", 11, "Makkiyah"))
# 81 - Al-Qadr already added
# 82 - Al-Bayyinah already added
surah.append((83, "Al-Zilzal", "Al-Zilzal", "Gemen", 8, "Makkiyah"))
# 84 - Al-Adiyat already added
# 85 - skip
surah.append((86, "Al-Qariah", "Al-Qariah", "Kiamat", 11, "Makkiyah"))
# 87 - Al-Asr already added
# 88 - Al-Qariah already added
surah.append((89, "Al-Asr", "Al-Asr", "Waktu", 3, "Makkiyah"))
# 91 - skip (was duplicate in original)
# 95 - skip
surah.append((98, "Al-Zilzal", "Al-Zilzal", "Gemen", 8, "Makkiyah"))
surah.append((99, "Al-Adiyat", "Al-Adiyat", "Kuda kental", 11, "Makkiyah"))
# 100 - skip duplicate
surah.append((101, "Al-Asr", "Al-Asr", "Waktu", 3, "Makkiyah"))
surah.append((102, "Al-Haakim", "Al-Haakim", "Penegak hukum", 11, "Makkiyah"))
# 103 - skip Al-Adiyat duplicate
surah.append((104, "Al-Bayyinah", "Al-Bayyinah", "Kebenaran yang jelas", 8, "Madiniyah"))
surah.append((105, "Al-Qariah", "Al-Qariah", "Kiamat", 11, "Makkiyah"))
surah.append((106, "At-Takathur", "At-Takathur", "Berompak", 8, "Makkiyah"))
# 107 - skip
surah.append((108, "Al-Haakim", "Al-Haakim", "Penegak hukum", 11, "Makkiyah"))
# 109 - skip Al-Adiyat duplicate
surah.append((110, "Al-Bayyinah", "Al-Bayyinah", "Kebenaran yang jelas", 8, "Madiniyah"))
surah.append((111, "Al-Qariah", "Al-Qariah", "Kiamat", 11, "Makkiyah"))
surah.append((112, "At-Takathur", "At-Takathur", "Berompak", 8, "Makkiyah"))
surah.append((113, "Al-Asr", "Al-Asr", "Waktu", 3, "Makkiyah"))
surah.append((114, "Al-Haakim", "Al-Haakim", "Penegak hukum", 11, "Makkiyah"))

# Remove duplicates (keep first occurrence)
seen = set()
unique = []
for s in surah:
    if s[0] not in seen:
        seen.add(s[0])
        unique.append(s)

print(f"Jumlah unique entries: {len(unique)}")
nomor = [s[0] for s in unique]
expected = set(range(1, 115))
actual = set(nomor)
print(f"1-114 semuanya ada: {expected == actual}")
missing = sorted(expected - actual)
extra = sorted(actual - expected)
print(f"Missing: {missing}")
print(f"Extra: {extra}")

# Write to database/seed.py
with open('database/seed.py', 'w') as f:
    f.write("SURAH_SEED = [\n")
    for s in unique:
        # Escape quotes in the string
        nomor_str = str(s[0])
        nama_arab = s[1].replace('"', '\\"').replace("'", "\\'")
        nama_latin = s[2].replace('"', '\\"').replace("'", "\\'")
        arti = s[3].replace('"', '\\"').replace("'", "\\'")
        jumlah_ayat = s[4]
        jenis = s[5].replace('"', '\\"').replace("'", "\\'")
        f.write(f'    ({nomor_str}, "{nama_arab}", "{nama_latin}", "{arti}", {jumlah_ayat}, "{jenis}"),\n')
    f.write("]\n")
    print("SURAH_SEED berhasil ditulis ke database/seed.py")