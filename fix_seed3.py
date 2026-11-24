#!/usr/bin/env python
import sys
sys.path.insert(0, '.')
from database.seed import SURAH_SEED

# Current state: 107 entries, missing 35, 36, 57, 90, 92, 93, 94
# And surah 37 is Ghafir but should be As-Saffat

# Create a dict from current seed for easy manipulation
current = {s[0]: s for s in SURAH_SEED}

# Fix: change surah 37 from Ghafir to As-Saffat
current[37] = (37, "As-Saffat", "As-Saffat", "Barisan", 182, "Makkiyah")

# Add the 7 missing surah
current[35] = (35, "Ghafir", "Al-Ghafir", "Mengampun", 85, "Makkiyah")
current[36] = (36, "Ya-Sin", "Ya-Sin", "Ya-Sin", 83, "Makkiyah")
current[57] = (57, "Al-Hadid", "Al-Hadid", "Besi", 29, "Madiniyah")
current[90] = (90, "Al-Adiyat", "Al-Adiyat", "Kuda kental", 11, "Makkiyah")
current[92] = (92, "Al-Inshiqaq", "Al-Inshiqaq", "Pemisahan", 19, "Makkiyah")
current[93] = (93, "Al-Inshirah", "Al-Inshirah", "Perluasan", 8, "Makkiyah")
current[94] = (94, "Al-Balad", "Al-Balad", "Kota", 11, "Makkiyah")

# Remove any entries with nomor > 114 or duplicates
# Keep only nomor 1-114, first occurrence
seen = set()
filtered = []
for s in current.values():
    if s[0] not in seen and 1 <= s[0] <= 114:
        seen.add(s[0])
        filtered.append(s)

# Sort by nomor
filtered.sort(key=lambda x: x[0])

print(f"Jumlah setelah fix: {len(filtered)}")
nomor = [s[0] for s in filtered]
expected = set(range(1, 115))
actual = set(nomor)
print(f"1-114 semuanya ada: {expected == actual}")
missing = expected - actual
extra = actual - expected
print(f"Missing: {missing}")
print(f"Extra: {extra}")

# Write to database/seed.py
with open('database/seed.py', 'w') as f:
    f.write("SURAH_SEED = [\n")
    for s in filtered:
        f.write("    " + str(s) + ",\n")
    f.write("]\n")

print("Sudah ditulis ke database/seed.py")
PYEOF
writefile.py