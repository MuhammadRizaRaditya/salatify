"""View Splash Screen."""

from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import BackgroundColorBehavior
from kivy.graphics import Color, Rectangle
from utils.constants import (
    APP_NAME, APP_TAGLINE, COLOR_PRIMARY, COLOR_BACKGROUND, COLOR_ACCENT
)


class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "splash"
        self.md_bg_color = COLOR_PRIMARY
        self._build_ui()

    def _build_ui(self):
        layout = MDBoxLayout(orientation="vertical", spacing="20dp", padding="40dp")
        layout.md_bg_color = COLOR_PRIMARY

        with layout.canvas.before:
            Color(*self._hex_to_rgb(COLOR_BACKGROUND))
            self.bg_rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_bg, pos=self._update_bg)

        self.logo = Image(
            source="assets/images/logo.png",
            size_hint=(None, None),
            size=("120dp", "120dp"),
            pos_hint={"center_x": 0.5},
            allow_stretch=True,
        )

        self.lbl_app = MDLabel(
            text=APP_NAME,
            halign="center",
            theme_text_color="Custom",
            text_color=COLOR_BACKGROUND,
            font_style="Headline",
            bold=True,
        )
        self.lbl_tagline = MDLabel(
            text=APP_TAGLINE,
            halign="center",
            theme_text_color="Custom",
            text_color=COLOR_ACCENT,
            font_style="Title",
        )

        layout.add_widget(self.logo)
        layout.add_widget(self.lbl_app)
        layout.add_widget(self.lbl_tagline)
        self.add_widget(layout)

        # Animasi fade-in logo
        self.logo.opacity = 0
        anim = Animation(opacity=1, duration=1.0) + Animation(opacity=1, duration=1.5)
        anim.start(self.logo)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    @staticmethod
    def _hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4)) + (1.0,)

    def on_enter(self, *args):
        # Pindah ke login setelah 3 detik
        Clock.schedule_once(lambda dt: self._go_next(), 3.0)

    def _go_next(self):
        self.manager.current = "login"
