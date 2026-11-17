"""View Al-Qur'an dan Murottal."""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import MDSnackbar as Snackbar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from utils.constants import COLOR_PRIMARY, COLOR_ACCENT, COLOR_TEXT


class QuranScreen(Screen):
    def __init__(self, quran_controller, audio_service, **kwargs):
        super().__init__(**kwargs)
        self.name = "quran"
        self.ctrl = quran_controller
        self.audio = audio_service
        self._build_ui()

    def _build_ui(self):
        self.root = MDBoxLayout(orientation="vertical")
        self.root.md_bg_color = "#F7F8F5"
        self.add_widget(self.root)

    def on_enter(self, *args):
        self.root.clear_widgets()
        self._render()

    def _render(self):
        scroll = MDScrollView()
        box = MDBoxLayout(orientation="vertical", spacing="12dp", padding="16dp",
                          size_hint_y=None, height="900dp")
        box.md_bg_color = "#F7F8F5"

        title = MDLabel(text="Al-Qur'an", halign="left", theme_text_color="Custom",
                        text_color=COLOR_PRIMARY,             font_style="Headline", bold=True,
                        size_hint_y=None, height="40dp")

        self.field_cari = MDTextField(hint_text="Cari surah...",         mode="filled",
                                      size_hint_y=None, height="48dp")
        self.field_cari.bind(text=self._on_cari)

        self.daftar_box = MDBoxLayout(orientation="vertical", spacing="8dp",
                                      size_hint_y=None, height="650dp")

        box.add_widget(title)
        box.add_widget(self.field_cari)
        box.add_widget(self.daftar_box)
        scroll.add_widget(box)
        self.root.add_widget(scroll)
        self._load_surah()

    def _on_cari(self, instance, value):
        self._load_surah(q=value)

    def _load_surah(self, q=None):
        self.daftar_box.clear_widgets()
        daftar = self.ctrl.daftar_surah(q=q)
        if not daftar:
            self.daftar_box.add_widget(MDLabel(text="Surah tidak ditemukan.",
                                               halign="center", theme_text_color="Custom",
                                               text_color=COLOR_TEXT, size_hint_y=None, height="40dp"))
            return
        for s in daftar:
            card = MDCard(size_hint_y=None, height="64dp", padding="10dp", radius=[12, 12, 12, 12])
            card.md_bg_color = "#FFFFFF"
            w = MDBoxLayout(orientation="vertical", spacing="2dp")
            w1 = MDLabel(text=f"{s.nomor}. {s.nama_latin}", halign="left", theme_text_color="Custom",
                         text_color=COLOR_PRIMARY,             font_style="Title", bold=True,
                         size_hint_y=None, height="22dp")
            w2 = MDLabel(text=f"{s.nama_arab} • {s.jumlah_ayat} ayat • {s.jenis}",
                         halign="left", theme_text_color="Custom",
                         text_color=COLOR_TEXT,             font_style="Label", size_hint_y=None, height="18dp")
            w.add_widget(w1)
            w.add_widget(w2)
            card.add_widget(w)
            card.bind(on_press=lambda x, sid=s.id: self._pilih_surah(sid))
            self.daftar_box.add_widget(card)

    def _pilih_surah(self, surah_id):
        s = self.ctrl.detail(surah_id)
        if not s:
            Snackbar(text="Data surah tidak tersedia.").open()
            return
        # Audio murottal: contoh URL placeholder (legal source perlu diisi)
        url = f"https://cdn.jsdelivr.net/aria/mp3/{s.nomor:03d}.mp3"
        ok = self.audio.play(url)
        if ok:
            Snackbar(text=f"Memutar {s.nama_latin} (audio eksternal).").open()
        else:
            Snackbar(text="Audio tidak dapat diputar. Sumber audio belum tersedia.").open()
