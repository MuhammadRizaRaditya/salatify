"""View Pengaturan."""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import MDSnackbar as Snackbar
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText
from utils.constants import COLOR_PRIMARY, COLOR_ACCENT, COLOR_TEXT, APP_NAME, APP_TAGLINE, DEVELOPERS


class SettingsScreen(Screen):
    def __init__(self, auth_controller, **kwargs):
        super().__init__(**kwargs)
        self.name = "settings"
        self.auth = auth_controller
        self._build_ui()

    def _build_ui(self):
        self.root = MDBoxLayout(orientation="vertical")
        self.root.md_bg_color = "#F7F8F5"
        self.add_widget(self.root)

    def on_enter(self, *args):
        self.root.clear_widgets()
        self._render()

    def _render(self):
        box = MDBoxLayout(orientation="vertical", spacing="12dp", padding="16dp")
        box.md_bg_color = "#F7F8F5"

        title = MDLabel(text="Pengaturan", halign="left", theme_text_color="Custom",
                        text_color=COLOR_PRIMARY,             font_style="Headline", bold=True,
                        size_hint_y=None, height="40dp")

        card = MDCard(size_hint_y=None, height="320dp", padding="16dp", radius=[16, 16, 16, 16])
        card.md_bg_color = "#FFFFFF"
        cbox = MDBoxLayout(orientation="vertical", spacing="14dp")

        btn_tema = MDButton(MDButtonText(text="Toggle Tema Gelap/Terang"), style="filled", size_hint_y=None, height="44dp")
        btn_tema.bind(on_press=self._toggle_tema)
        row_tema = MDBoxLayout(orientation="horizontal", size_hint_y=None, height="40dp")
        row_tema.add_widget(MDLabel(text="Tema Gelap", halign="left", theme_text_color="Custom",
                                    text_color=COLOR_TEXT, size_hint_x=0.7))
        row_tema.add_widget(btn_tema)

        btn_profil = MDButton(MDButtonText(text="Profil Pengguna"), style="text", size_hint_y=None, height="40dp")
        btn_profil.bind(on_press=lambda x: Snackbar(text="Profil: fitur edit profil.").open())

        btn_notif = MDButton(MDButtonText(text="Pengaturan Notifikasi"), style="text", size_hint_y=None, height="40dp")
        btn_notif.bind(on_press=lambda x: Snackbar(text="Pengaturan notifikasi sholat.").open())

        btn_loc = MDButton(MDButtonText(text="Lokasi & Metode Sholat"), style="text", size_hint_y=None, height="40dp")
        btn_loc.bind(on_press=lambda x: setattr(self.manager, "current", "prayer"))

        cbox.add_widget(row_tema)
        cbox.add_widget(btn_profil)
        cbox.add_widget(btn_notif)
        cbox.add_widget(btn_loc)
        card.add_widget(cbox)

        card2 = MDCard(size_hint_y=None, height="220dp", padding="16dp", radius=[16, 16, 16, 16])
        card2.md_bg_color = "#FFFFFF"
        cbox2 = MDBoxLayout(orientation="vertical", spacing="12dp")
        lbl_tentang = MDLabel(text="Tentang Aplikasi", halign="left", theme_text_color="Custom",
                              text_color=COLOR_PRIMARY,             font_style="Title", bold=True,
                              size_hint_y=None, height="28dp")
        lbl_nama = MDLabel(text=APP_NAME, halign="left", theme_text_color="Custom",
                           text_color=COLOR_TEXT,             font_style="Body", size_hint_y=None, height="24dp")
        lbl_tagline = MDLabel(text=APP_TAGLINE, halign="left", theme_text_color="Custom",
                              text_color=COLOR_ACCENT, font_style="Caption", size_hint_y=None, height="20dp")
        lbl_dev = MDLabel(text="Dikembangkan oleh: " + ", ".join(DEVELOPERS),
                          halign="left", theme_text_color="Custom", text_color=COLOR_TEXT,
                          font_style="Label", size_hint_y=None, height="24dp")
        lbl_ver = MDLabel(text=f"Versi {APP_NAME.split()[-1] if False else '1.0.0'}",
                          halign="left", theme_text_color="Custom", text_color=COLOR_TEXT,
                          font_style="Label", size_hint_y=None, height="20dp")

        cbox2.add_widget(lbl_tentang)
        cbox2.add_widget(lbl_nama)
        cbox2.add_widget(lbl_tagline)
        cbox2.add_widget(lbl_dev)
        cbox2.add_widget(lbl_ver)
        card2.add_widget(cbox2)

        btn_keluar = MDButton(MDButtonText(text="Keluar"), style="filled", size_hint_y=None, height="44dp")
        btn_keluar.bind(on_press=self._keluar)

        box.add_widget(title)
        box.add_widget(card)
        box.add_widget(card2)
        box.add_widget(btn_keluar)
        self.root.add_widget(box)

    def _toggle_tema(self, instance, value):
        # Placeholder untuk tema gelap/terang
        pass

    def _keluar(self, *args):
        self.auth.logout()
        self.manager.current = "login"
