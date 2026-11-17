"""View Dashboard."""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.snackbar import MDSnackbar as Snackbar
from kivy.clock import Clock
from utils.constants import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT, COLOR_TEXT, PRAYER_LABELS


class DashboardScreen(Screen):
    def __init__(self, dashboard_controller, **kwargs):
        super().__init__(**kwargs)
        self.name = "dashboard"
        self.ctrl = dashboard_controller
        self._build_ui()
        Clock.schedule_interval(self._update_jam, 1.0)

    def _build_ui(self):
        self.root = MDBoxLayout(orientation="vertical")
        self.root.md_bg_color = "#F7F8F5"
        self.add_widget(self.root)

    def on_enter(self, *args):
        self.root.clear_widgets()
        self._render()

    def _render(self):
        scroll = MDScrollView()
        box = MDBoxLayout(orientation="vertical", spacing="15dp", padding="20dp",
                          size_hint_y=None, height="820dp")
        box.md_bg_color = "#F7F8F5"

        nama = getattr(self.ctrl.current_user, "username", "Pengguna") if hasattr(self.ctrl, "current_user") else "Pengguna"

        lbl_salam = MDLabel(text=self.ctrl.salam(nama), halign="left", theme_text_color="Custom",
                            text_color=COLOR_PRIMARY,             font_style="Headline", bold=True, size_hint_y=None, height="40dp")
        lbl_tgl = MDLabel(text=self.ctrl.tanggal_masehi(), halign="left", theme_text_color="Custom",
                          text_color=COLOR_TEXT,             font_style="Body", size_hint_y=None, height="30dp")
        self.lbl_jam = MDLabel(text=self.ctrl.jam_digital(), halign="left", theme_text_color="Custom",
                               text_color=COLOR_ACCENT,             font_style="Title", bold=True, size_hint_y=None, height="30dp")

        # Card jadwal sholat
        card = MDCard(size_hint_y=None, height="200dp", padding="15dp", radius=[16, 16, 16, 16])
        card.md_bg_color = "#FFFFFF"
        cbox = MDBoxLayout(orientation="vertical", spacing="8dp")
        ctitle = MDLabel(text="Jadwal Sholat Hari Ini", halign="left", theme_text_color="Custom",
                         text_color=COLOR_PRIMARY,             font_style="Title", bold=True, size_hint_y=None, height="30dp")
        self.lbl_countdown = MDLabel(text="--:--", halign="left", theme_text_color="Custom",
                                     text_color=COLOR_ACCENT,             font_style="Title", bold=True, size_hint_y=None, height="30dp")
        self.lbl_sholat_berikut = MDLabel(text="--", halign="left", theme_text_color="Custom",
                                          text_color=COLOR_TEXT,             font_style="Body", size_hint_y=None, height="24dp")

        grid = MDGridLayout(cols=5, spacing="8dp", size_hint_y=None, height="90dp")
        for key in ["subuh", "dzuhur", "ashar", "maghrib", "isya"]:
            w = MDBoxLayout(orientation="vertical", size_hint_y=None, height="80dp")
            w.md_bg_color = "#F0F4F1"
            w.radius = [10, 10, 10, 10]
            lb = MDLabel(text=PRAYER_LABELS[key], halign="center", theme_text_color="Custom",
                         text_color=COLOR_TEXT,             font_style="Label", size_hint_y=None, height="20dp")
            lt = MDLabel(text="--:--", halign="center", theme_text_color="Custom",
                         text_color=COLOR_PRIMARY,             font_style="Title", bold=True, size_hint_y=None, height="24dp")
            lt.name_key = key
            w.add_widget(lb)
            w.add_widget(lt)
            grid.add_widget(w)
            setattr(self, f"w_{key}", lt)

        cbox.add_widget(ctitle)
        cbox.add_widget(grid)
        cbox.add_widget(self.lbl_sholat_berikut)
        cbox.add_widget(self.lbl_countdown)
        card.add_widget(cbox)

        # Tombol akses cepat
        grid_btn = MDGridLayout(cols=2, spacing="12dp", size_hint_y=None, height="220dp")
        for teks, target in [("Jadwal Sholat", "prayer"), ("Arah Kiblat", "qibla"),
                             ("Dzikir", "dzikir"), ("Kumpulan Doa", "doa"),
                             ("Al-Qur'an", "quran"), ("Pengaturan", "settings")]:
            b = MDButton(MDButtonText(text=teks), style="filled", size_hint_y=None, height="48dp")
            b.bind(on_press=lambda x, t=target: setattr(self.manager, "current", t))
            grid_btn.add_widget(b)

        box.add_widget(lbl_salam)
        box.add_widget(lbl_tgl)
        box.add_widget(self.lbl_jam)
        box.add_widget(card)
        box.add_widget(MDLabel(text="Akses Cepat", halign="left", theme_text_color="Custom",
                               text_color=COLOR_PRIMARY,             font_style="Title", bold=True,
                               size_hint_y=None, height="30dp"))
        box.add_widget(grid_btn)

        scroll.add_widget(box)
        self.root.add_widget(scroll)
        self._refresh_jadwal()

    def _refresh_jadwal(self):
        from services.location_service import LocationService
        jadwal = self.ctrl.jadwal_hari_ini("-6.2", "106.8", "mwml")
        for key, widget in [("subuh", self.w_subuh), ("dzuhur", self.w_dzuhur),
                            ("ashar", self.w_ashar), ("maghrib", self.w_maghrib), ("isya", self.w_isya)]:
            widget.text = jadwal.get(key, "--:--")
        nama, sisa, waktu = self.ctrl.countdown_berikutnya(jadwal)
        if nama:
            self.lbl_sholat_berikut.text = f"Sholat berikutnya: {PRAYER_LABELS[nama]}"
            self.lbl_countdown.text = self.ctrl.hitung_countdown(waktu)
        else:
            self.lbl_sholat_berikut.text = "Jadwal sholat tersimpan offline"
            self.lbl_countdown.text = "--:--"

    def _update_jam(self, *args):
        if not hasattr(self, "lbl_jam"):
            return
        self.lbl_jam.text = self.ctrl.jam_digital()
        # perbarui countdown setiap detik
        jadwal = self.ctrl.jadwal_hari_ini("-6.2", "106.8", "mwml")
        nama, sisa, waktu = self.ctrl.countdown_berikutnya(jadwal)
        if nama and waktu:
            self.lbl_countdown.text = self.ctrl.hitung_countdown(waktu)
            self.lbl_sholat_berikut.text = f"Sholat berikutnya: {PRAYER_LABELS[nama]}"
