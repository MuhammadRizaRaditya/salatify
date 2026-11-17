"""View Detail Doa."""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import MDSnackbar as Snackbar
from kivymd.uix.scrollview import MDScrollView
from kivy.core.clipboard import Clipboard
from utils.constants import COLOR_PRIMARY, COLOR_ACCENT, COLOR_TEXT


class DoaDetailScreen(Screen):
    def __init__(self, doa_controller, **kwargs):
        super().__init__(**kwargs)
        self.name = "doa_detail"
        self.ctrl = doa_controller
        self.doa = None
        self._build_ui()

    def _build_ui(self):
        self.root = MDBoxLayout(orientation="vertical")
        self.root.md_bg_color = "#F7F8F5"
        self.add_widget(self.root)

    def tampilkan(self, doa):
        self.doa = doa
        self.root.clear_widgets()
        self._render()

    def _render(self):
        scroll = MDScrollView()
        box = MDBoxLayout(orientation="vertical", spacing="12dp", padding="16dp",
                          size_hint_y=None, height="700dp")
        box.md_bg_color = "#F7F8F5"

        title = MDLabel(text=self.doa.judul if self.doa else "Doa",
                        halign="left", theme_text_color="Custom",
                        text_color=COLOR_PRIMARY,             font_style="Headline", bold=True,
                        size_hint_y=None, height="40dp")

        card = MDCard(size_hint_y=None, height="300dp", padding="18dp", radius=[16, 16, 16, 16])
        card.md_bg_color = "#FFFFFF"
        cbox = MDBoxLayout(orientation="vertical", spacing="8dp")

        lab_arab = MDLabel(text="Arab", halign="left", theme_text_color="Custom",
                           text_color=COLOR_ACCENT,             font_style="Title", bold=True,
                           size_hint_y=None, height="20dp")
        txt_arab = MDLabel(text=self.doa.arab if self.doa else "",
                           halign="center", theme_text_color="Custom",
                           text_color=COLOR_TEXT,             font_style="Body", size_hint_y=None, height="60dp")

        lab_latin = MDLabel(text="Latin", halign="left", theme_text_color="Custom",
                            text_color=COLOR_ACCENT,             font_style="Title", bold=True,
                            size_hint_y=None, height="20dp")
        txt_latin = MDLabel(text=self.doa.latin if self.doa else "",
                            halign="left", theme_text_color="Custom",
                            text_color=COLOR_TEXT,             font_style="Body", size_hint_y=None, height="40dp")

        lab_terj = MDLabel(text="Terjemahan", halign="left", theme_text_color="Custom",
                           text_color=COLOR_ACCENT,             font_style="Title", bold=True,
                           size_hint_y=None, height="20dp")
        txt_terj = MDLabel(text=self.doa.terjemahan if self.doa else "",
                           halign="left", theme_text_color="Custom",
                           text_color=COLOR_TEXT,             font_style="Body", size_hint_y=None, height="60dp")

        lab_ref = MDLabel(text=f"Referensi: {self.doa.referensi}" if self.doa and self.doa.referensi else "Referensi: -",
                          halign="left", theme_text_color="Custom",
                          text_color=COLOR_TEXT,             font_style="Title", size_hint_y=None, height="20dp")

        cbox.add_widget(lab_arab)
        cbox.add_widget(txt_arab)
        cbox.add_widget(lab_latin)
        cbox.add_widget(txt_latin)
        cbox.add_widget(lab_terj)
        cbox.add_widget(txt_terj)
        cbox.add_widget(lab_ref)
        card.add_widget(cbox)

        btn_fav = MDButton(MDButtonText(text="Favorit"), style="filled", size_hint_y=None, height="44dp")
        btn_fav.bind(on_press=self._toggle_fav)

        btn_salin = MDButton(MDButtonText(text="Salin Teks"), style="text", size_hint_y=None, height="40dp")
        btn_salin.bind(on_press=self._salin)

        btn_kembali = MDButton(MDButtonText(text="Kembali"), style="text", size_hint_y=None, height="40dp")
        btn_kembali.bind(on_press=lambda x: setattr(self.manager, "current", "doa"))

        box.add_widget(title)
        box.add_widget(card)
        box.add_widget(btn_fav)
        box.add_widget(btn_salin)
        box.add_widget(btn_kembali)
        scroll.add_widget(box)
        self.root.add_widget(scroll)

    def _toggle_fav(self, *args):
        if self.ctrl.toggle_favorit(self.doa.id):
            Snackbar(text="Ditambahkan ke favorit.").open()
        else:
            Snackbar(text="Dihapus dari favorit.").open()

    def _salin(self, *args):
        teks = f"{self.doa.arab}\n{self.doa.latin}\n{self.doa.terjemahan}"
        Clipboard.copy(teks)
        Snackbar(text="Teks disalin ke papan klip.").open()
