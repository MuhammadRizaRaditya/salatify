"""View Kumpulan Doa."""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import MDSnackbar as Snackbar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivy.core.clipboard import Clipboard
from utils.constants import COLOR_PRIMARY, COLOR_ACCENT, COLOR_TEXT


class DoaScreen(Screen):
    def __init__(self, doa_controller, **kwargs):
        super().__init__(**kwargs)
        self.name = "doa"
        self.ctrl = doa_controller
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
                          size_hint_y=None, height="850dp")
        box.md_bg_color = "#F7F8F5"

        title = MDLabel(text="Kumpulan Doa", halign="left", theme_text_color="Custom",
                        text_color=COLOR_PRIMARY,             font_style="Headline", bold=True,
                        size_hint_y=None, height="40dp")

        self.field_cari = MDTextField(hint_text="Cari doa...",         mode="filled",
                                      size_hint_y=None, height="48dp")
        self.field_cari.bind(text=self._on_cari)

        self.daftar_box = MDBoxLayout(orientation="vertical", spacing="8dp",
                                      size_hint_y=None, height="600dp")

        box.add_widget(title)
        box.add_widget(self.field_cari)
        box.add_widget(self.daftar_box)
        scroll.add_widget(box)
        self.root.add_widget(scroll)
        self._load_doa()

    def _on_cari(self, instance, value):
        self._load_doa(q=value)

    def _load_doa(self, q=None):
        self.daftar_box.clear_widgets()
        daftar = self.ctrl.daftar_doa(q=q)
        if not daftar:
            self.daftar_box.add_widget(MDLabel(text="Doa tidak ditemukan.",
                                               halign="center", theme_text_color="Custom",
                                               text_color=COLOR_TEXT,
                                               size_hint_y=None, height="40dp"))
            return
        for doa in daftar:
            card = MDCard(size_hint_y=None, height="72dp", padding="10dp", radius=[12, 12, 12, 12])
            card.md_bg_color = "#FFFFFF"
            w = MDBoxLayout(orientation="vertical", spacing="2dp")
            w1 = MDLabel(text=doa.judul, halign="left", theme_text_color="Custom",
                         text_color=COLOR_PRIMARY,             font_style="Title", bold=True,
                         size_hint_y=None, height="22dp")
            w2 = MDLabel(text=doa.terjemahan or "", halign="left", theme_text_color="Custom",
                         text_color=COLOR_TEXT,             font_style="Label", size_hint_y=None, height="18dp")
            w.add_widget(w1)
            w.add_widget(w2)
            card.add_widget(w)
            card.bind(on_press=lambda x, d=doa: self._buka_detail(d))
            self.daftar_box.add_widget(card)

    def _buka_detail(self, doa):
        self.manager.get_screen("doa_detail").tampilkan(doa)
        self.manager.current = "doa_detail"
