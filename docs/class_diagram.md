# Class Diagram (Mermaid)

Diagram kelas aplikasi SALATIFY dengan arsitektur MVC, meliputi model database, controller/service, tampilan screen, serta backend FastAPI.

---

## 1. Model (Database)

Diagram ini menampilkan 11 tabel database beserta atribut dan relasi antar tabel dengan multiplicity (1, 0..*).

```mermaid
direction TB
classDiagram
    class User {
        +id: int PK
        +username: varchar(100) unique
        +email: varchar(150) unique
        +password_hash: varchar(255)
        +is_guest: bool default false
        +is_active: bool default true
        +created_at: datetime
    }
    class JadwalSholat {
        +id: int PK
        +tanggal: varchar(20)
        +subuh: varchar(10)
        +dzuhur: varchar(10)
        +ashar: varchar(10)
        +maghrib: varchar(10)
        +isya: varchar(10)
        +lokasi: varchar(200)
        +latitude: varchar(50)
        +longitude: varchar(50)
        +metode: varchar(50)
        +perbarui_pada: datetime
    }
    class PrayerPreferences {
        +id: int PK
        +user_id: int FK unique
        +lokasi: varchar(200)
        +latitude: varchar(50)
        +longitude: varchar(50)
        +metode: varchar(50)
        +zona_waktu: varchar(100)
        +pengingat_aktif: bool default true
        +pengingat_offset: int default 0
        +suara_aktif: bool default true
        +getaran_aktif: bool default true
    }
    class KategoriDoa {
        +id: int PK
        +nama: varchar(100) unique
        +label: varchar(100)
    }
    class Doa {
        +id: int PK
        +kategori_id: int FK
        +judul: varchar(200)
        +arab: text
        +latin: text
        +terjemahan: text
        +referensi: text
        +diverifikasi: int default 1
    }
    class FavoriteDoa {
        +id: int PK
        +user_id: int FK
        +doa_id: int FK
    }
    class Dzikir {
        +id: int PK
        +kategori: varchar(50)
        +judul: varchar(200)
        +arab: text
        +latin: text
        +terjemahan: text
        +jumlah_dianjurkan: int
    }
    class DzikirHistory {
        +id: int PK
        +user_id: int FK
        +dzikir_id: int
        +jumlah: int default 0
        +tanggal: datetime
    }
    class Surah {
        +id: int PK
        +nomor: int unique
        +nama_arab: varchar(100)
        +nama_latin: varchar(100)
        +arti: varchar(100)
        +jumlah_ayat: int
        +jenis: varchar(20)
    }
    class FavoriteSurah {
        +id: int PK
        +user_id: int FK
        +surah_id: int FK
    }
    class UserSettings {
        +id: int PK
        +user_id: int FK unique
        +tema_gelap: bool default false
        +nama_lengkap: varchar(150)
        +email: varchar(150)
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

---

## 2. Controller dan Service

Diagram ini menampilkan 7 controller dan 6 service beserta dependensi antarnya menggunakan panah `..>`.

```mermaid
direction LR
classDiagram
    class AuthController {
        +register(username, email, password): bool
        +login(username_or_email, password): bool
        +login_guest(): bool
        +logout(): bool
        +change_password(old_password, new_password): bool
    }
    class DashboardController {
        +salam(nama): str
        +tanggal_masehi(): str
        +tanggal_hijriah(): str
        +jam_digital(): str
        +jadwal_hari_ini(lat, lon, metode): dict
        +countdown_berikutnya(jadwal): tuple
        +ringkasan_dzikir(): int
    }
    class PrayerController {
        +get_preferences(): PrayerPreferences
        +save_preferences(lokasi, lat, lon, metode, zona_waktu, pengingat_aktif, offset, suara, getaran): PrayerPreferences
        +ambil_jadwal(lat, lon, metode, tanggal): dict
        +jadwal_offline(tanggal): dict
        +hitung_countdown(waktu_str): str
    }
    class QiblaController {
        +hitung_bearing(lat_user, lon_user): float
        +arah_teks(derajat): str
    }
    class DzikirController {
        +daftar_dzikir(kategori=None): list
        +simpan_tasbih(jumlah, dzikir_id): bool
        +riwayat(limit=20): list
    }
    class DoaController {
        +daftar_kategori(): list
        +daftar_doa(kategori=None, q=None): list
        +detail(doa_id): Doa
        +is_favorit(doa_id): bool
        +toggle_favorit(doa_id): bool
    }
    class QuranController {
        +daftar_surah(q=None): list
        +detail(surah_id): Surah
        +toggle_favorit(surah_id): bool
    }
    class PrayerService {
        +get_timings(latitude, longitude, metode, tanggal): dict
    }
    class QiblaService {
        +bearing_kiblat(lat_user, lon_user): float
    }
    class LocationService {
        +start(): bool
        +stop(): None
    }
    class NotificationService {
        +kirim(judul, pesan, timeout): bool
        +pengingat_sholat(nama_sholat, waktu): bool
    }
    class QuranService {
        +daftar_surah(): list
    }
    class AudioService {
        +play(url): bool
        +stop(): None
        +playing: bool
    }

    AuthController ..> PrayerService : gunakan
    DashboardController ..> PrayerService : gunakan
    DashboardController ..> DzikirHistory : query
    PrayerController ..> PrayerService : gunakan
    PrayerController ..> PrayerPreferences : query/save
    PrayerController ..> JadwalSholat : query/save
    QiblaController ..> QiblaService : gunakan
    QiblaController ..> LocationService : ambil lokasi
    DzikirController ..> Dzikir : query
    DzikirController ..> User : query history
    DzikirController ..> DzikirHistory : simpan/query
    DoaController ..> KategoriDoa : query
    DoaController ..> Doa : query
    DoaController ..> FavoriteDoa : toggle favorit
    DoaController ..> User : cek user_id
    QuranController ..> QuranService : ambil data
    QuranController ..> FavoriteSurah : toggle favorit
    QuranController ..> Surah : query
    QuranController ..> AudioService : play murottal
    AuthController ..> SalatifyApiClient : (opsional) sync ke backend
```

---

## 3. View (Screen)

Diagram ini menampilkan hubungan setiap screen (UI) dengan controller-nya di dalam penumpang ScreenManager Kivy.

```mermaid
direction LR
classDiagram
    class SplashScreen
    class LoginScreen
    class RegisterScreen
    class DashboardScreen
    class PrayerScreen
    class QiblaScreen
    class DzikirScreen
    class DoaScreen
    class QuranScreen
    class SettingsScreen

    SplashScreen --> LoginScreen : pindah setelah 3 detik
    LoginScreen --> DashboardScreen : login sukses
    RegisterScreen --> LoginScreen : daftar akun baru
    DashboardScreen --> AuthController : salam, jam, jadwal
    PrayerScreen --> PrayerController : jadwal, countdown, preferensi
    QiblaScreen --> QiblaController : bearing, arah kiblat
    QiblaScreen --> LocationService : sensor GPS
    DzikirScreen --> DzikirController : tasbih, riwayat
    DoaScreen --> DoaController : daftar doa, favorit, detail
    QuranScreen --> QuranController : daftar surah, favorit, audio
    QuranScreen --> AudioService : play murottal
    SettingsScreen --> AuthController : logout, tema, profil
```

---

## 4. Backend FastAPI

Diagram ini menampilkan router, schema, model SQLAlchemy, dan ApiClient di services/api_client.py.

```mermaid
direction TB
classDiagram
    class RouterAuth {
        +post("/auth/register"): UserOut
        +post("/auth/login"): Token
        +post("/auth/guest"): Token
        +get("/auth/me"): UserOut
        +post("/auth/logout"): message
    }
    class RouterUsers {
        +get("/users/me"): UserOut
        +put("/users/password"): message
        +get("/users/settings"): UserSettingsOut
        +put("/users/settings"): UserSettingsOut
    }
    class RouterDoa {
        +get("/doa/kategori"): list[KategoriDoaOut]
        +get("/doa"): list[DoaOut]
        +get("/doa/{doa_id}"): DoaOut
        +post("/doa/{doa_id}/favorit"): dict
    }
    class RouterDzikir {
        +get("/dzikir"): list[DzikirOut]
        +get("/dzikir/riwayat"): list[DzikirHistoryOut]
        +post("/dzikir/riwayat"): DzikirHistoryOut
    }
    class RouterPrayer {
        +get("/prayer/jadwal"): PrayerTimeOut
        +get("/prayer/jadwal/{tanggal}"): PrayerTimeOut
        +get("/prayer/preferensi"): PrayerPreferencesOut
        +put("/prayer/preferensi"): PrayerPreferencesOut
    }
    class RouterQibla {
        +post("/qibla/hitung"): QiblaResponse
    }
    class RouterQuran {
        +get("/quran/surah"): list[SurahOut]
        +get("/quran/surah/{surah_id}"): SurahOut
        +post("/quran/surah/{surah_id}/favorit"): dict
        +get("/quran/api/surah"): dict
    }
    class RouterReminder {
        +get("/reminder"): PrayerPreferencesOut
        +put("/reminder"): PrayerPreferencesOut
    }

    class UserRegister
    class UserLogin
    class Token
    class UserOut
    class KategoriDoaOut
    class DoaOut
    class DzikirOut
    class DzikirHistoryIn
    class DzikirHistoryOut
    class PrayerTimeOut
    class PrayerPreferencesIn
    class PrayerPreferencesOut
    class PasswordChange
    class UserSettingsIn
    class UserSettingsOut
    class SurahOut
    class QiblaRequest
    class QiblaResponse

    RouterAuth -- UserRegister : request
    RouterAuth -- UserLogin : request
    RouterAuth -- Token : response
    RouterAuth -- UserOut : response
    RouterUsers -- UserOut : response
    RouterUsers -- UserSettingsIn : request
    RouterUsers -- UserSettingsOut : response
    RouterDoa -- KategoriDoaOut : response
    RouterDoa -- DoaOut : response
    RouterDoa -- PasswordChange : request
    RouterDzikir -- DzikirOut : response
    RouterDzikir -- DzikirHistoryIn : request
    RouterDzikir -- DzikirHistoryOut : response
    RouterPrayer -- PrayerTimeOut : response
    RouterPrayer -- PrayerPreferencesIn : request
    RouterPrayer -- PrayerPreferencesOut : response
    RouterQibla -- QiblaRequest : request
    RouterQibla -- QiblaResponse : response
    RouterQuran -- SurahOut : response
    RouterQuran -- QiblaRequest : request (api/surah)
    RouterReminder -- PrayerPreferencesOut : response

    class SalatifyApiClient {
        +base_url: str
        +timeout: int
        +token: str
        +register(username, email, password): Dict
        +login(username_or_email, password): Dict
        +login_guest(): Dict
        +me(): Dict
        +logout(): Dict
        +daftar_doa(kategori, q): list
        +detail_doa(doa_id): Dict
        +toggle_favorit_doa(doa_id): Dict
        +daftar_dzikir(kategori): list
        +riwayat_dzikir(): list
        +simpan_tasbih(jumlah, dzikir_id): Dict
        +jadwal_hari_ini(lat, lon, metode, tanggal): Dict
        +preferensi(): Dict
        +set_preferensi(payload): Dict
        +hitung_kiblat(lat, lon): Dict
        +daftar_surah(q): list
        +detail_surah(surah_id): Dict
        +toggle_favorit_surah(surah_id): Dict
        +profil(): Dict
        +settings(): Dict
        +update_settings(payload): Dict
        +_headers(): Dict
        +_get(path, params): Any
        +_post(path, json): Any
        +_put(path, json): Any
    }
```