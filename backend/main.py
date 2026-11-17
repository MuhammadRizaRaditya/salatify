"""Aplikasi FastAPI SALATIFY - Backend bersama untuk Android dan Website."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from backend.database import engine, Base, init_db
from backend import models  # noqa: F401  (daftarkan model ke Base)
from backend.routers import auth, users, doa, dzikir, prayer, qibla, quran, reminder
from backend.seed import run_seed

app = FastAPI(
    title="SALATIFY API",
    description="Backend bersama untuk aplikasi Android dan website SALATIFY — Smart Islamic Companion",
    version="1.0.0",
)

# CORS untuk mengizinkan Android (WebView) dan website memanggil API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dalam produksi ganti dengan domain yang tepat
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router API
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(doa.router)
app.include_router(dzikir.router)
app.include_router(prayer.router)
app.include_router(qibla.router)
app.include_router(quran.router)
app.include_router(reminder.router)


@app.on_event("startup")
def on_startup():
    init_db()
    run_seed()


@app.get("/health")
def health():
    return {"status": "ok", "app": "SALATIFY"}


@app.get("/")
def root():
    return {
        "message": "Selamat datang di SALATIFY API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/manifest.json")
def manifest():
    return FileResponse(os.path.join(WEB_DIR, "manifest.json"))


@app.get("/sw.js")
def sw():
    return FileResponse(os.path.join(WEB_DIR, "sw.js"))


# --- Frontend Website (PWA/static HTML) ---
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "web")
STATIC_DIR = os.path.join(WEB_DIR, "static")
PAGES_DIR = os.path.join(WEB_DIR, "pages")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
# Keep cached pages using the former relative asset URLs working during rollout.
app.mount("/web/static", StaticFiles(directory=STATIC_DIR), name="web-static-compat")


def _page(file_name: str):
    path = os.path.join(PAGES_DIR, file_name)
    if os.path.exists(path):
        return FileResponse(path)
    return {"error": "Halaman tidak ditemukan"}


@app.get("/web")
def web_home():
    return _page("index.html")


@app.get("/web/{page}.html")
def web_page(page: str):
    return _page(f"{page}.html")
