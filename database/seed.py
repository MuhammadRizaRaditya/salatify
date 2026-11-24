"""Seeder data awal: kategori doa, doa, dzikir, dan surah.
Dapat dijalankan berulang kali tanpa duplikasi (idempotent)."""

from sqlalchemy.orm import Session

from backend.models import KategoriDoa, Doa, Dzikir, Surah


DOA_SEED = [
    {
        "kategori": "sebelum_makan",
        "judul": "Doa Sebelum Makan",
        "arab": "بِسْمِ اللَّهِ وَعَلَى بَرَكَةِ اللَّهِ",
        "latin": "Bismillah wa 'ala barakatillah",
        "terjemahan": "Dengan nama Allah dan dengan berkah Allah.",
        "referensi": "Hadits",
    },
    {
        "kategori": "setelah_makan",
        "judul": "Doa Sesudah Makan",
        "arab": "الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنَا وَسَقَانَا وَجَعَلَنَا مِنَ الْمُسْلِمِينَ",
        "latin": "Alhamdulillah alladhi at'amana wa saqana wa ja'alana minal muslimina",
        "terjemahan": "Segala puji bagi Allah yang telah memberi kita makan dan minum, dan menjadikan kita umat Muslim.",
        "referensi": "Hadits",
    },
    {
        "kategori": "sebelum_tidur",
        "judul": "Doa Sebelum Tidur",
        "arab": "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا",
        "latin": "Bismika allahumma amutu wa ahya",
        "terjemahan": "Dengan nama-Mu ya Allah, aku mati dan aku hidup.",
        "referensi": "Hadits Bukhari & Muslim",
    },
    {
        "kategori": "bangun_tidur",
        "judul": "Doa Bangun Tidur",
        "arab": "الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَىهِ النُّشُورُ",
        "latin": "Alhamdulillah alladhi ahyana ba'da ma amatana wa ilayhin-nushur",
        "terjemahan": "Segala puji bagi Allah yang telah menghidupkan kita setelah mematikan kita, dan kepada-Nyalah kebangkitan.",
        "referensi": "Hadits Bukhari",
    },
    {
        "kategori": "masuk_rumah",
        "judul": "Doa Masuk Rumah",
        "arab": "بِسْمِ اللَّهِ وَلَجْنَا وَبِسْمِ اللَّهِ خَرَجْنَا وَعَلَى رَبِّنَا Tَوَكَّلْنَا",
        "latin": "Bismillah walajna wa bismillah kharajna wa 'ala rabbina tawakkalna",
        "terjemahan": "Dengan nama Allah kita masuk, dengan nama Allah kita keluar, dan pada Tuhan kami kita bertawakkal.",
        "referensi": "Hadits Abu Daud",
    },
    {
        "kategori": "keluar_rumah",
        "judul": "Doa Keluar Rumah",
        "arab": "بِسْمِ اللَّهِ تَوَكَّلْتُ عَلَى لَّا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ",
        "latin": "Bismillah tawakkalta 'alallah la haula wa la quwwata illa billah",
        "terjemahan": "Dengan nama Allah, aku bertawakkal kepada Allah, tidak ada daya dan kuasa kecuali dengan Allah.",
        "referensi": "Hadits Tirmidzi",
    },
    {
        "kategori": "masuk_kamar_mandi",
        "judul": "Doa Masuk Kamar Mandi",
        "arab": "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْخُبْثِ وَالْخَبَائِثِ",
        "latin": "Allahumma inni a'udhu bika minal khubthi wal khaba'ith",
        "terjemahan": "Ya Allah, aku berlindung-Mu dari keji-keji dan makhluk keji.",
        "referensi": "Hadits Bukhari & Muslim",
    },
    {
        "kategori": "keluar_kamar_mandi",
        "judul": "Doa Keluar Kamar Mandi",
        "arab": "غُفْرَانَكَ",
        "latin": "Ghufranak",
        "terjemahan": "Aku memohon ampunan-Mu.",
        "referensi": "Hadits Tirmidzi",
    },
    {
        "kategori": "bepergian",
        "judul": "Doa Bepergian",
        "arab": "سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَذَا وَمَا كُنَّا لَهُ مُقْرِنِينَ وَإِنَّا إِلَى رَبِّنَا لَمُنقَلِبُونَ",
        "latin": "Subhanalladhi sakhkhara lana hadha wa ma kunna lahu muqrinina wa inna ila rabbina lamunqalibuna",
        "terjemahan": "Maha suci Allah yang telah menundukkan ini kepada kita dan kita sebelumnya tidak mampu menguasainya, dan sesungguhnya kepada Tuhan kami kita akan kembali.",
        "referensi": "QS. Az-Zukhruf 43:13-14",
    },
    {
        "kategori": "memohon_ilmu",
        "judul": "Doa Memohon Ilmu",
        "arab": "رَبِّ زِدْنِي عِلْمًا",
        "latin": "Rabbizidni 'ilman",
        "terjemahan": "Ya Tuhan, Tambahkanlah aku ilmu.",
        "referensi": "QS. Thaha 20:114",
    },
    {
        "kategori": "orang_tua",
        "judul": "Doa untuk Kedua Orang Tua",
        "arab": "رَبِّ ارْحَمْهُمَا كَمَا رَبَّيَانِي صَغِيرًا",
        "latin": "Rabbirhamhuma kama rabbayani saghira",
        "terjemahan": "Ya Tuhan, sayangiilah keduanya sebagaimana mereka mendidik saya ketika kecil.",
        "referensi": "QS. Al-Isra 17:24",
    },
    {
        "kategori": "setelah_sholat",
        "judul": "Doa Setelah Sholat",
        "arab": "أَسْتَغْفِرُ اللَّهَ (3x) اللَّهُمَّ أَنْتَ السَّلَامُ وَمِنْكَ السَّلَامُ تَبَارَكْتَ يَا ذَا الْجَلَالِ وَالْإِكْرَامِ",
        "latin": "Astaghfirullah (3x) Allahumma antas-salamu wa minka-s-salamu tabarakta ya dhal-jalali wal-ikram",
        "terjemahan": "Aku memohon ampunan kepada Allah (3x). Ya Allah, Engkau adalah Keselamatan dan dari-Mulah keselamatan, Maha Suci ya Pemilik keagungan dan kemuliaan.",
        "referensi": "Hadits Muslim",
    },
    {
        "kategori": "bercermin",
        "judul": "Doa Bercermin",
        "arab": "اللَّهُمَّ كَمَا أَحْسَنْتَ خَلْقِي فَحَسِّنْ خُلُقِي",
        "latin": "Allahumma kama ahsanta khalqi fa-hassan khuluqi",
        "terjemahan": "Ya Allah, sebagaimana Engkau telah indahkan ciptaan saya, maka indahkanlah akhlak saya.",
        "referensi": "Hadits",
    },
    {
        "kategori": "saat_hujan",
        "judul": "Doa Ketika Hujan",
        "arab": "اللَّهُمَّ صَيِّبًا نَافِعًا",
        "latin": "Allahumma sayyiban nafi'an",
        "terjemahan": "Ya Allah, hujan yang bermanfaat.",
        "referensi": "Hadits Bukhari",
    },
]


DHIKIR_SEED = [
    {
        "kategori": "setelah_sholat",
        "judul": "Tasbih Fatimah",
        "arab": "سُبْحَانَ اللَّهِ (33x) الْحَمْدُ لِلَّهِ (33x) اللَّهُ أَكْبَرُ (34x)",
        "latin": "Subhanallah (33x) Alhamdulillah (33x) Allahu Akbar (34x)",
        "terjemahan": "Maha suci Allah (33x), Segala puji bagi Allah (33x), Allah Mahabesar (34x).",
        "jumlah_dianjurkan": 100,
    },
    {
        "kategori": "pagi",
        "judul": "Dzikir Pagi",
        "arab": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ رَبِّ الْعَالَمِينَ",
        "latin": "Asbahna wa asbaha al-mulku lillahi rabbil 'alamina",
        "terjemahan": "Kita telah menjadi pagi dan seluruh kerajaan milik Allah Tuhan alam semesta.",
        "jumlah_dianjurkan": 1,
    },
    {
        "kategori": "petang",
        "judul": "Dzikir Petang",
        "arab": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ رَبِّ الْعَالَمِينَ",
        "latin": "Amsayna wa amsa al-mulku lillahi rabbil 'alamina",
        "terjemahan": "Kita telah menjadi petang dan seluruh kerajaan milik Allah Tuhan alam semesta.",
        "jumlah_dianjurkan": 1,
    },
    {
        "kategori": "istighfar",
        "judul": "Istighfar",
        "arab": "أَسْتَغْفِرُ اللَّهَ رَبِّي مِنْ كُلِّ ذَنْبٍ وَأَتُوبُ إِلَيْهِ",
        "latin": "Astaghirullah rabbi min kulli dzinbin wa atubu ilayh",
        "terjemahan": "Aku memohon ampunan kepada Allah, Tuhanku, dari segala dosa, dan aku bertobat kepada-Nya.",
        "jumlah_dianjurkan": 100,
    },
    {
        "kategori": "sholawat",
        "judul": "Sholawat Ibrahimiyyah",
        "arab": "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ وَعَلَى آلِ مُحَمَّدٍ كَمَا صَلَّيْتَ عَلَى إِبْرَاهِيمَ وَعَلَى آلِ إِبْرَاهِيمَ",
        "latin": "Allahumma sholli 'ala Muhammadin wa 'ala ali Muhammadin kama shallaita 'ala Ibrahima wa 'ala ali Ibrahima",
        "terjemahan": "Ya Allah, berilah shalawat kepada Muhammad dan keluarga Muhammad sebagaimana Engkau memberi shalawat kepada Ibrahim dan keluarga Ibrahim.",
        "jumlah_dianjurkan": 10,
    },
]


# SURAH_SEED: 114 surah Al-Qur'an dengan nomor 1-114
# Setiap entry: (nomor, nama_arab, nama_latin, arti, jumlah_ayat, jenis)
SURAH_SEED = [
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


def run_seed(db):
    # Kategori doa
    for item in DOA_SEED:
        existing = db.query(KategoriDoa).filter_by(nama=item["kategori"]).first()
        if not existing:
            db.add(KategoriDoa(nama=item["kategori"], label=item["judul"]))
    db.commit()
    kategori_map = {k.nama: k.id for k in db.query(KategoriDoa).all()}

    # Doa
    for item in DOA_SEED:
        existing = db.query(Doa).filter_by(arab=item["arab"]).first()
        if not existing:
            db.add(Doa(
                kategori_id=kategori_map[item["kategori"]],
                judul=item["judul"], arab=item["arab"], latin=item["latin"],
                terjemahan=item["terjemahan"], referensi=item["referensi"],
            ))
    db.commit()

    # Dzikir
    for item in DHIKIR_SEED:
        existing = db.query(Dzikir).filter_by(arab=item["arab"]).first()
        if not existing:
            db.add(Dzikir(
                kategori=item["kategori"], judul=item["judul"], arab=item["arab"],
                latin=item["latin"], terjemahan=item["terjemahan"],
                jumlah_dianjurkan=item["jumlah_dianjurkan"],
            ))
    db.commit()

    # Surah
    for nomor, nama_arab, nama_latin, arti, jumlah_ayat, jenis in SURAH_SEED:
        existing = db.query(Surah).filter_by(nomor=nomor).first()
        if not existing:
            db.add(Surah(
                nomor=nomor, nama_arab=nama_arab, nama_latin=nama_latin,
                arti=arti, jumlah_ayat=jumlah_ayat, jenis=jenis,
            ))
    db.commit()