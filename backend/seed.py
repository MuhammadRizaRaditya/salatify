"""Seeder data awal untuk backend PostgreSQL (idempoten)."""

from backend.database import SessionLocal, engine
from backend import models
from backend.models import KategoriDoa, Doa, Dzikir, Surah

DOA_SEED = [
    {"kategori": "sebelum_makan", "judul": "Doa Sebelum Makan",
     "arab": "بِسْمِ اللَّهِ وَعَلَى بَرَكَةِ اللَّهِ",
     "latin": "Bismillah wa 'ala barakatillah",
     "terjemahan": "Dengan nama Allah dan dengan berkah Allah.", "referensi": "Hadits"},
    {"kategori": "setelah_makan", "judul": "Doa Sesudah Makan",
     "arab": "الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنَا وَسَقَانَا وَجَعَلَنَا مِنَ الْمُسْلِمِينَ",
     "latin": "Alhamdulillah alladhi at'amana wa saqana wa ja'alana minal muslimina",
     "terjemahan": "Segala puji bagi Allah yang telah memberi kita makan dan minum, dan menjadikan kita umat Muslim.", "referensi": "Hadits"},
    {"kategori": "sebelum_tidur", "judul": "Doa Sebelum Tidur",
     "arab": "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا",
     "latin": "Bismika allahumma amutu wa ahya",
     "terjemahan": "Dengan nama-Mu ya Allah, aku mati dan aku hidup.", "referensi": "Hadits Bukhari & Muslim"},
    {"kategori": "bangun_tidur", "judul": "Doa Bangun Tidur",
     "arab": "الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ",
     "latin": "Alhamdulillah alladhi ahyana ba'da ma amatana wa ilayhin-nushur",
     "terjemahan": "Segala puji bagi Allah yang telah menghidupkan kita setelah mematikan kita, dan kepada-Nyalah kebangkitan.", "referensi": "Hadits Bukhari"},
    {"kategori": "masuk_rumah", "judul": "Doa Masuk Rumah",
     "arab": "بِسْمِ اللَّهِ وَلَجْنَا وَبِسْمِ اللَّهِ خَرَجْنَا وَعَلَى رَبِّنَا تَوَكَّلْنَا",
     "latin": "Bismillah walajna wa bismillah kharajna wa 'ala rabbina tawakkalna",
     "terjemahan": "Dengan nama Allah kita masuk, dengan nama Allah kita keluar, dan pada Tuhan kami kita bertawakkal.", "referensi": "Hadits Abu Daud"},
    {"kategori": "keluar_rumah", "judul": "Doa Keluar Rumah",
     "arab": "بِسْمِ اللَّهِ تَوَكَّلْتُ عَلَى اللَّهِ لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ",
     "latin": "Bismillah tawakkalta 'alallah la haula wa la quwwata illa billah",
     "terjemahan": "Dengan nama Allah, aku bertawakkal kepada Allah, tidak ada daya dan kuasa kecuali dengan Allah.", "referensi": "Hadits Tirmidzi"},
    {"kategori": "masuk_kamar_mandi", "judul": "Doa Masuk Kamar Mandi",
     "arab": "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْخُبْثِ وَالْخَبَائِثِ",
     "latin": "Allahumma inni a'udhu bika minal khubthi wal khaba'ith",
     "terjemahan": "Ya Allah, aku berlindung-Mu dari keji-keji dan makhluk keji.", "referensi": "Hadits Bukhari & Muslim"},
    {"kategori": "keluar_kamar_mandi", "judul": "Doa Keluar Kamar Mandi",
     "arab": "غُفْرَانَكَ",
     "latin": "Ghufranak",
     "terjemahan": "Aku memohon ampunan-Mu.", "referensi": "Hadits Tirmidzi"},
    {"kategori": "bepergian", "judul": "Doa Bepergian",
     "arab": "سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَذَا وَمَا كُنَّا لَهُ مُقْرِنِينَ وَإِنَّا إِلَى رَبِّنَا لَمُنقَلِبُونَ",
     "latin": "Subhanalladhi sakhkhara lana hadha wa ma kunna lahu muqrinina wa inna ila rabbina lamunqalibuna",
     "terjemahan": "Maha suci Allah yang telah menundukkan ini kepada kita dan kita sebelumnya tidak mampu menguasainya, dan kepada Tuhan kami kita akan kembali.", "referensi": "QS. Az-Zukhruf 43:13-14"},
    {"kategori": "memohon_ilmu", "judul": "Doa Memohon Ilmu",
     "arab": "رَبِّ زِدْنِي عِلْمًا",
     "latin": "Rabbizidni 'ilman",
     "terjemahan": "Ya Tuhan, tambahkanlah aku ilmu.", "referensi": "QS. Thaha 20:114"},
    {"kategori": "orang_tua", "judul": "Doa untuk Kedua Orang Tua",
     "arab": "رَبِّ ارْحَمْهُمَا كَمَا رَبَّيَانِي صَغِيرًا",
     "latin": "Rabbirhamhuma kama rabbayani saghira",
     "terjemahan": "Ya Tuhan, sayangiilah keduanya sebagaimana mereka mendidik saya ketika kecil.", "referensi": "QS. Al-Isra 17:24"},
    {"kategori": "setelah_sholat", "judul": "Doa Setelah Sholat",
     "arab": "أَسْتَغْفِرُ اللَّهَ (3x) اللَّهُمَّ أَنْتَ السَّلَامُ وَمِنْكَ السَّلَامُ تَبَارَكْتَ يَا ذَا الْجَلَالِ وَالْإِكْرَامِ",
     "latin": "Astaghfirullah (3x) Allahumma antas-salamu wa minka-s-salamu tabarakta ya dhal-jalali wal-ikram",
     "terjemahan": "Aku memohon ampunan kepada Allah (3x). Ya Allah, Engkau adalah Keselamatan dan dari-Mulah keselamatan, Maha Suci ya Pemilik keagungan dan kemuliaan.", "referensi": "Hadits Muslim"},
    {"kategori": "bercermin", "judul": "Doa Bercermin",
     "arab": "اللَّهُمَّ كَمَا أَحْسَنْتَ خَلْقِي فَحَسِّنْ خُلُقِي",
     "latin": "Allahumma kama ahsanta khalqi fa-hassan khuluqi",
     "terjemahan": "Ya Allah, sebagaimana Engkau telah indahkan ciptaan saya, maka indahkanlah akhlak saya.", "referensi": "Hadits"},
    {"kategori": "saat_hujan", "judul": "Doa Ketika Hujan",
     "arab": "اللَّهُمَّ صَيِّبًا نَافِعًا",
     "latin": "Allahumma sayyiban nafi'an",
     "terjemahan": "Ya Allah, hujan yang bermanfaat.", "referensi": "Hadits Bukhari"},
]

DHIKIR_SEED = [
    {"kategori": "setelah_sholat", "judul": "Tasbih Fatimah",
     "arab": "سُبْحَانَ اللَّهِ (33x) الْحَمْدُ لِلَّهِ (33x) اللَّهُ أَكْبَرُ (34x)",
     "latin": "Subhanallah (33x) Alhamdulillah (33x) Allahu Akbar (34x)",
     "terjemahan": "Maha suci Allah (33x), Segala puji bagi Allah (33x), Allah Mahabesar (34x).",
     "jumlah_dianjurkan": 100},
    {"kategori": "pagi", "judul": "Dzikir Pagi",
     "arab": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ رَبِّ الْعَالَمِينَ",
     "latin": "Asbahna wa asbaha al-mulku lillahi rabbil 'alamina",
     "terjemahan": "Kita telah menjadi pagi dan seluruh kerajaan milik Allah Tuhan alam semesta.",
     "jumlah_dianjurkan": 1},
    {"kategori": "petang", "judul": "Dzikir Petang",
     "arab": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ رَبِّ الْعَالَمِينَ",
     "latin": "Amsayna wa amsa al-mulku lillahi rabbil 'alamina",
     "terjemahan": "Kita telah menjadi petang dan seluruh kerajaan milik Allah Tuhan alam semesta.",
     "jumlah_dianjurkan": 1},
    {"kategori": "istighfar", "judul": "Istighfar",
     "arab": "أَسْتَغْفِرُ اللَّهَ رَبِّي مِنْ كُلِّ ذَنْبٍ وَأَتُوبُ إِلَيْهِ",
     "latin": "Astaghfirullah rabbi min kulli dzinbin wa atubu ilayh",
     "terjemahan": "Aku memohon ampunan kepada Allah, Tuhanku, dari segala dosa, dan aku bertobat kepada-Nya.",
     "jumlah_dianjurkan": 100},
    {"kategori": "sholawat", "judul": "Sholawat Ibrahimiyyah",
     "arab": "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ وَعَلَى آلِ مُحَمَّدٍ كَمَا صَلَّيْتَ عَلَى إِبْرَاهِيمَ وَعَلَى آلِ إِبْرَاهِيمَ",
     "latin": "Allahumma sholli 'ala Muhammadin wa 'ala ali Muhammadin kama shallaita 'ala Ibrahima wa 'ala ali Ibrahima",
     "terjemahan": "Ya Allah, berilah shalawat kepada Muhammad dan keluarga Muhammad sebagaimana Engkau memberi shalawat kepada Ibrahim dan keluarga Ibrahim.",
     "jumlah_dianjurkan": 10},
]

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
]


def run_seed():
    db = SessionLocal()
    try:
        for item in DOA_SEED:
            existing = db.query(KategoriDoa).filter_by(nama=item["kategori"]).first()
            if not existing:
                db.add(KategoriDoa(nama=item["kategori"], label=item["judul"]))
        db.commit()
        kategori_map = {k.nama: k.id for k in db.query(KategoriDoa).all()}

        for item in DOA_SEED:
            existing = db.query(Doa).filter_by(arab=item["arab"]).first()
            if not existing:
                db.add(Doa(
                    kategori_id=kategori_map[item["kategori"]],
                    judul=item["judul"], arab=item["arab"], latin=item["latin"],
                    terjemahan=item["terjemahan"], referensi=item["referensi"],
                ))
        db.commit()

        for item in DHIKIR_SEED:
            existing = db.query(Dzikir).filter_by(arab=item["arab"]).first()
            if not existing:
                db.add(Dzikir(
                    kategori=item["kategori"], judul=item["judul"], arab=item["arab"],
                    latin=item["latin"], terjemahan=item["terjemahan"],
                    jumlah_dianjurkan=item["jumlah_dianjurkan"],
                ))
        db.commit()

        for nomor, nama_arab, nama_latin, arti, jumlah_ayat, jenis in SURAH_SEED:
            existing = db.query(Surah).filter_by(nomor=nomor).first()
            if not existing:
                db.add(Surah(
                    nomor=nomor, nama_arab=nama_arab, nama_latin=nama_latin,
                    arti=arti, jumlah_ayat=jumlah_ayat, jenis=jenis,
                ))
        db.commit()
        print("Seeder backend selesai.")
    finally:
        db.close()


if __name__ == "__main__":
    from backend.database import Base
    Base.metadata.create_all(bind=engine)
    run_seed()
