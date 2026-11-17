"""View Wirid dan Dzikir + Tasbih digital."""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import MDSnackbar as Snackbar
from kivymd.uix.scrollview import MDScrollView
from kivy.clock import Clock
from utils.constants import COLOR_PRIMARY, COLOR_ACCENT, COLOR_TEXT


class DzikirScreen(Screen):
    def __init__(self, dzikir_controller, **kwargs):
        super().__init__(**kwargs)
        self.name = "dzikir"
        self.ctrl = dzikir_controller
        self.hitungan = 0
        self.target = 100
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
        box = MDBoxLayout(orientation="vertical", spacing="15dp", padding="20dp",
                          size_hint_y=None, height="700dp")
        box.md_bg_color = "#F7F8F5"

        title = MDLabel(text="Dzikir & Tasbih", halign="left", theme_text_color="Custom",
                        text_color=COLOR_PRIMARY,             font_style="Headline", bold=True,
                        size_hint_y=None, height="40dp")

        card = MDCard(size_hint_y=None, height="220dp", padding="20dp", radius=[20, 20, 20, 20])
        card.md_bg_color = "#FFFFFF"
        cbox = MDBoxLayout(orientation="vertical", spacing="10dp")

        self.lbl_judul = MDLabel(text="Tasbih Fatimah", halign="center", theme_text_color="Custom",
                                 text_color=COLOR_PRIMARY,             font_style="Headline", bold=True,
                                 size_hint_y=None, height="30dp")
        self.lbl_hitung = MDLabel(text="0", halign="center", theme_text_color="Custom",
                                  text_color=COLOR_PRIMARY,             font_style="Headline", bold=True,
                                  size_hint_y=None, height="90dp")
        self.lbl_progres = MDLabel(text="0 / 100", halign="center", theme_text_color="Custom",
                                   text_color=COLOR_TEXT,             font_style="Body", size_hint_y=None, height="24dp")

        btn_tambah = MDButton(MDButtonText(text="+ Tambah"), style="filled",
                              size_hint_y=None, height="44dp")
        btn_tambah.bind(on_press=self._tambah)
        btn_reset = MDButton(MDButtonText(text="Reset"), style="text",
                             size_hint_y=None, height="40dp")
        btn_reset.bind(on_press=self._reset)

        cbox.add_widget(self.lbl_judul)
        cbox.add_widget(self.lbl_hitung)
        cbox.add_widget(self.lbl_progres)
        cbox.add_widget(btn_tambah)
        cbox.add_widget(btn_reset)
        card.add_widget(cbox)

        box.add_widget(title)
        box.add_widget(card)
        scroll.add_widget(box)
        self.root.add_widget(scroll)

    def _tambah(self, *args):
        self.hitungan += 1
        self.lbl_hitung.text = str(self.hitungan)
        self.lbl_progres.text = f"{self.hitungan} / {self.target}"
        if self.hitungan >= self.target:
            Snackbar(text="Target tercapai! Barakallahu fiik.").open()
            self.hitungan = 0
            self.lbl_hitung.text = "0"
            self.lbl_progres.text = f"0 / {self.target}"
            self.ctrl.simpan_tasbih(self.target)
        else:
            self.ctrl.simpan_tasbih(self.hitungan)

    def _reset(self, *args):
        self.hitungan = 0
        self.lbl_hitung.text = "0"
        self.lbl_progres.text = f"0 / {self.target}"
