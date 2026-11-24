#!/usr/bin/env python
import requests
import json

# Fetch surah data from equran.id API
resp = requests.get('https://equran.id/api/v2/surah', timeout=15)
data = resp.json()

# Create SURAH_SEED list: (nomor, nama_arab, nama_latin, arti, jumlah_ayat, jenis)
surah_seed = []
for item in data["data"]:
    nomor = item["nomor"]
    nama_arab = item["nama_arab"]
    nama_latin = item["nama_latin"]
    arti = item["arti"] if "arti" in item else ""
    jumlah_ayat = item["jumlah_ayat"] if "jumlah_ayat" in item else 0
    jenis = item["jenis"] if "jenis" in item else "Makkiyah"
    surah_seed.append((nomor, nama_arab, nama_latin, arti, jumlah_ayat, jenis))

# Remove duplicates (keep first occurrence)
seen = set()
unique = []
for s in surah_seed:
    if s[0] not in seen:
        seen.add(s[0])
        unique.append(s)

print(f"Jumlah total dari API: {len(surah_seed)}")
print(f"Jumlah unique: {len(unique)}")
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
        # Escape any special characters in the arti (string)
        arti_escaped = s[3].replace('\\', '\\\\').replace("'", r"\'") if s[3] else ""
        f.write(f"    {s},\n")
    f.write("]\n")

print("Sudah ditulis ke database/seed.py")