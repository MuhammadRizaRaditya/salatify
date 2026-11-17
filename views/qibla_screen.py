"""View Arah Kiblat (kompas digital)."""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import MDSnackbar as Snackbar
from kivy.graphics import PushMatrix, PopMatrix, Rotate
from kivy.animation import Animation
from kivy.clock import Clock
from utils.constants import COLOR_PRIMARY, COLOR_ACCENT, COLOR_TEXT


class QiblaScreen(Screen):
    def __init__(self, qibla_controller, location_service, **kwargs):
        super().__init__(**kwargs)
        self.name = "qibla"
        self.ctrl = qibla_controller
        self.loc = location_service
        self.derajat = 0.0
        self._build_ui()

    def _build_ui(self):
        self.root = MDBoxLayout(orientation="vertical")
        self.root.md_bg_color = "#F7F8F5"
        self.add_widget(self.root)

    def on_enter(self, *args):
        self.root.clear_widgets()
        self._render()
        self.loc.start()

    def on_leave(self, *args):
        self.loc.stop()

    def _render(self):
        box = MDBoxLayout(orientation="vertical", spacing="15dp", padding="20dp")
        box.md_bg_color = "#F7F8F5"

        title = MDLabel(text="Arah Kiblat", halign="left", theme_text_color="Custom",
                        text_color=COLOR_PRIMARY,             font_style="Headline", bold=True,
                        size_hint_y=None, height="40dp")

        card = MDCard(size_hint_y=None, height="300dp", padding="15dp", radius=[24, 24, 24, 24])
        card.md_bg_color = "#FFFFFF"
        cbox = MDBoxLayout(orientation="vertical", spacing="10dp")

        self.lbl_derajat = MDLabel(text="0°", halign="center", theme_text_color="Custom",
                                   text_color=COLOR_PRIMARY,             font_style="Headline", bold=True,
                                   size_hint_y=None, height="80dp")
        self.lbl_arah = MDLabel(text="--", halign="center", theme_text_color="Custom",
                                text_color=COLOR_TEXT, font_style="Subtitle1", bold=True,
                                size_hint_y=None, height="30dp")
        self.lbl_status = MDLabel(text="Menunggu sensor...", halign="center", theme_text_color="Custom",
                                  text_color=COLOR_ACCENT, font_style="Caption", size_hint_y=None, height="24dp")

        cbox.add_widget(self.lbl_derajat)
        cbox.add_widget(self.lbl_arah)
        cbox.add_widget(self.lbl_status)
        card.add_widget(cbox)

        btn_kalibrasi = MDButton(MDButtonText(text="Kalibrasi Kompas"), style="filled",
                                 size_hint_y=None, height="44dp")
        btn_kalibrasi.bind(on_press=self._kalibrasi)

        box.add_widget(title)
        box.add_widget(card)
        box.add_widget(btn_kalibrasi)
        self.root.add_widget(box)

    def _kalibrasi(self, *args):
        self.loc.start()
        Snackbar(text="Putar perangkat dalam pola 8 untuk kalibrasi kompas.").open()

    def update_location(self, loc):
        lat = loc.get("lat")
        lon = loc.get("lon")
        if lat and lon:
            derajat = self.ctrl.hitung_bearing(lat, lon)
            if derajat is not None:
                self.derajat = derajat
                self.lbl_derajat.text = f"{derajat}°"
                self.lbl_arah.text = self.ctrl.arah_teks(derajat)
                self.lbl_status.text = f"Lokasi: {lat}, {lon}"

    def update_compass(self, bearing):
        # bearing: arah perangkat relatif Utara (derajat)
        # Kompas menunjuk kiblat: putar agar 0° sejajar kiblat
        self.lbl_status.text = f"Sensor orientasi: {bearing}°"
