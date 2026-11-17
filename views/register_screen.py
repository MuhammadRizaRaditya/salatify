"""View Register Screen."""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar as Snackbar
from utils.constants import COLOR_PRIMARY


class RegisterScreen(Screen):
    def __init__(self, auth_controller, **kwargs):
        super().__init__(**kwargs)
        self.name = "register"
        self.auth = auth_controller
        self._build_ui()

    def _build_ui(self):
        layout = MDBoxLayout(orientation="vertical", spacing="15dp", padding="30dp")
        layout.md_bg_color = "#F7F8F5"

        lbl = MDLabel(
            text="Daftar",
            halign="center",
            theme_text_color="Custom",
            text_color=COLOR_PRIMARY,
            font_style="Title",
            bold=True,
            size_hint_y=None,
            height="40dp",
        )

        self.field_user = MDTextField(hint_text="Username",         mode="filled", size_hint_y=None, height="50dp")
        self.field_email = MDTextField(hint_text="Email",         mode="filled", size_hint_y=None, height="50dp")
        self.field_pass = MDTextField(hint_text="Password",         mode="filled", password=True, size_hint_y=None, height="50dp")
        self.field_conf = MDTextField(hint_text="Konfirmasi Password",         mode="filled", password=True, size_hint_y=None, height="50dp")

        btn_daftar = MDButton(MDButtonText(text="Daftar"), style="filled", size_hint_y=None, height="45dp")
        btn_daftar.bind(on_press=self._do_register)

        btn_kembali = MDButton(MDButtonText(text="Kembali ke Masuk"), style="text", size_hint_y=None, height="40dp")
        btn_kembali.bind(on_press=lambda x: setattr(self.manager, "current", "login"))

        layout.add_widget(lbl)
        layout.add_widget(self.field_user)
        layout.add_widget(self.field_email)
        layout.add_widget(self.field_pass)
        layout.add_widget(self.field_conf)
        layout.add_widget(btn_daftar)
        layout.add_widget(btn_kembali)
        self.add_widget(layout)

    def _do_register(self, *args):
        if self.field_pass.text != self.field_conf.text:
            Snackbar(text="Konfirmasi password tidak cocok.").open()
            return
        ok, msg = self.auth.register(self.field_user.text, self.field_email.text, self.field_pass.text)
        Snackbar(text=msg).open()
        if ok:
            self.manager.current = "login"
