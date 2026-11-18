# Class Diagram (Mermaid)

Diagram kelas aplikasi SALATIFY dengan arsitektur MVC, meliputi model database, controller/service, tampilan screen, serta backend FastAPI.

---

## 1. Model (Database)

Diagram ini menampilkan 11 tabel database beserta relasi antar tabel dengan multiplicity (1, 0..*).

```mermaid
classDiagram
    class User {
        +id: int
        +username: string
        +email: string
        +password_hash: string
        +is_guest: bool
        +is_active: bool
        +created_at: string
    }
    class JadwalSholat {
        +id: int
        +tanggal: string
        +subuh: string
        +dzuhur: string
        +ashar: string
        +maghrib: string
        +isya: string
        +lokasi: string
        +latitude: string
        +longitude: string
        +metode: string
        +perbarui_pada: string
    }
    class PrayerPreferences {
        +id: int
        +user_id: int
        +lokasi: string
        +latitude: string
        +longitude: string
        +metode: string
        +zona_waktu: string
        +pengingat_aktif: bool
        +pengingat_offset: int
        +suara_aktif: bool
        +getaran_aktif: bool
    }
    class KategoriDoa {
        +id: int
        +nama: string
        +label: string
    }
    class Doa {
        +id: int
        +kategori_id: int
        +judul: string
        +arab: string
        +latin: string
        +terjemahan: string
        +referensi: string
        +diverifikasi: int
    }
    class FavoriteDoa {
        +id: int
        +user_id: int
        +doa_id: int
    }
    class Dzikir {
        +id: int
        +kategori: string
        +judul: string
        +arab: string
        +latin: string
        +terjemahan: string
        +jumlah_dianjurkan: int
    }
    class DzikirHistory {
        +id: int
        +user_id: int
        +dzikir_id: int
        +jumlah: int
        +tanggal: string
    }
    class Surah {
        +id: int
        +nomor: int
        +nama_arab: string
        +nama_latin: string
        +arti: string
        +jumlah_ayat: int
        +jenis: string
    }
    class FavoriteSurah {
        +id: int
        +user_id: int
        +surah_id: int
    }
    class UserSettings {
        +id: int
        +user_id: int
        +tema_gelap: bool
        +nama_lengkap: string
        +email: string
    }

    User "1" *-- "*" FavoriteDoa : doa_favorit
    User "1" *-- "*" FavoriteSurah : surah_favorit
    User "1" *-- "*" DzikirHistory : dzikir_history
    User "1" -- "*" PrayerPreferences : preferensi
    User "1" -- "*" UserSettings : settingan
    KategoriDoa "1" *-- "*" Doa : doa
    Doa "N" -- "1" KategoriDoa : kategori
    FavoriteDoa "N" -- "1" User : user
    FavoriteDoa "N" -- "1" Doa : doa
    DzikirHistory "N" -- "1" User : user
    DzikirHistory "N" -- "0..1" Dzikir : dzikir (opsional)
    FavoriteSurah "N" -- "1" User : user
    FavoriteSurah "N" -- "1" Surah : surah
    Surah "1" *-- "*" FavoriteSurah : favorit
    PrayerPreferences "1" -- "1" User : user
    UserSettings "1" -- "1" User : user
```