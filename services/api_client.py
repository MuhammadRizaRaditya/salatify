"""API Client untuk menghubungkan aplikasi Android SALATIFY ke backend FastAPI shared.

Catatan: Adapter ini TAMBAHAN dan OPSIONAL. Aplikasi Android tetap berfungsi
secara lokal dengan SQLite tanpa backend. Adapter hanya digunakan jika ingin
sinkronisasi data akun, doa favorit, surah favorit, dan riwayat dzikir ke
database bersama PostgreSQL agar bisa diakses juga dari website.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

try:
    import requests  # type: ignore
except Exception:  # pragma: no cover - requests tidak tersedia di semua build
    requests = None


class SalatifyApiClient:
    """Klien REST untuk backend SALATIFY (FastAPI)."""

    def __init__(self, base_url: str = "http://127.0.0.1:8000", timeout: int = 15):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.token: Optional[str] = None

    # ---------- Auth ----------
    def register(self, username: str, email: str, password: str) -> Dict[str, Any]:
        if requests is None:
            raise RuntimeError("library requests tidak tersedia")
        resp = requests.post(
            f"{self.base_url}/auth/register",
            json={"username": username, "email": email, "password": password},
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()

    def login(self, username_or_email: str, password: str) -> Dict[str, Any]:
        if requests is None:
            raise RuntimeError("library requests tidak tersedia")
        resp = requests.post(
            f"{self.base_url}/auth/login",
            json={"username": username_or_email, "password": password},
            timeout=self.timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        self.token = data.get("access_token")
        return data

    def login_guest(self) -> Dict[str, Any]:
        if requests is None:
            raise RuntimeError("library requests tidak tersedia")
        resp = requests.post(
            f"{self.base_url}/auth/guest", timeout=self.timeout
        )
        resp.raise_for_status()
        data = resp.json()
        self.token = data.get("access_token")
        return data

    def me(self) -> Dict[str, Any]:
        return self._get("/auth/me")

    def logout(self) -> Dict[str, Any]:
        self.token = None
        return self._post("/auth/logout")

    # ---------- Doa ----------
    def daftar_doa(self, kategori: Optional[str] = None, q: Optional[str] = None) -> list:
        params = {}
        if kategori:
            params["kategori"] = kategori
        if q:
            params["q"] = q
        return self._get("/doa", params=params)

    def detail_doa(self, doa_id: int) -> Dict[str, Any]:
        return self._get(f"/doa/{doa_id}")

    def toggle_favorit_doa(self, doa_id: int) -> Dict[str, Any]:
        return self._post(f"/doa/{doa_id}/favorit")

    # ---------- Dzikir ----------
    def daftar_dzikir(self, kategori: Optional[str] = None) -> list:
        params = {"kategori": kategori} if kategori else {}
        return self._get("/dzikir", params=params)

    def riwayat_dzikir(self) -> list:
        return self._get("/dzikir/riwayat")

    def simpan_tasbih(self, jumlah: int, dzikir_id: Optional[int] = None) -> Dict[str, Any]:
        return self._post("/dzikir/riwayat", json={"dzikir_id": dzikir_id, "jumlah": jumlah})

    # ---------- Jadwal Sholat ----------
    def jadwal_hari_ini(
        self, latitude: str, longitude: str, metode: str = "mwml", tanggal: Optional[str] = None
    ) -> Dict[str, Any]:
        params = {"latitude": latitude, "longitude": longitude, "metode": metode}
        if tanggal:
            params["tanggal"] = tanggal
        return self._get("/prayer/jadwal", params=params)

    def preferensi(self) -> Dict[str, Any]:
        return self._get("/prayer/preferensi")

    def set_preferensi(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._put("/prayer/preferensi", json=payload)

    # ---------- Qibla ----------
    def hitung_kiblat(self, latitude: float, longitude: float) -> Dict[str, Any]:
        return self._post("/qibla/hitung", json={"latitude": latitude, "longitude": longitude})

    # ---------- Al-Qur'an ----------
    def daftar_surah(self, q: Optional[str] = None) -> list:
        params = {"q": q} if q else {}
        return self._get("/quran/surah", params=params)

    def detail_surah(self, surah_id: int) -> Dict[str, Any]:
        return self._get(f"/quran/surah/{surah_id}")

    def toggle_favorit_surah(self, surah_id: int) -> Dict[str, Any]:
        return self._post(f"/quran/surah/{surah_id}/favorit")

    # ---------- Pengaturan ----------
    def profil(self) -> Dict[str, Any]:
        return self._get("/users/me")

    def settings(self) -> Dict[str, Any]:
        return self._get("/users/settings")

    def update_settings(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._put("/users/settings", json=payload)

    # ---------- Internal ----------
    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        if requests is None:
            raise RuntimeError("library requests tidak tersedia")
        resp = requests.get(
            f"{self.base_url}{path}", params=params, headers=self._headers(), timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        if requests is None:
            raise RuntimeError("library requests tidak tersedia")
        resp = requests.post(
            f"{self.base_url}{path}", json=json, headers=self._headers(), timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    def _put(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        if requests is None:
            raise RuntimeError("library requests tidak tersedia")
        resp = requests.put(
            f"{self.base_url}{path}", json=json, headers=self._headers(), timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()
