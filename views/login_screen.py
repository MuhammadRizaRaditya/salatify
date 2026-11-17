"""View Login Screen."""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar as Snackbar
from utils.constants import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT, COLOR_TEXT


class LoginScreen(Screen):
    def __init__(self, auth_controller, **kwargs):
        super().__init__(**kwargs)
        self.name = "login"
        self.auth = auth_controller
        self._build_ui()

    def _build_ui(self):
        layout = MDBoxLayout(orientation="vertical", spacing="15dp", padding="30dp")
        layout.md_bg_color = "#F7F8F5"

        lbl = MDLabel(
            text="Masuk",
            halign="center",
            theme_text_color="Custom",
            text_color=COLOR_PRIMARY,
            font_style="Title",
            bold=True,
            size_hint_y=None,
            height="40dp",
        )

        self.field_user = MDTextField(
            hint_text="Username atau Email",
            mode="filled",
            size_hint_y=None,
            height="50dp",
        )
        self.field_pass = MDTextField(
            hint_text="Password",
            mode="filled",
            password=True,
            size_hint_y=None,
            height="50dp",
        )

        btn_masuk = MDButton(
            MDButtonText(text="Masuk"),
            style="filled",
            size_hint_y=None,
            height="45dp",
        )
        btn_masuk.bind(on_press=self._do_login)

        btn_daftar = MDButton(
            MDButtonText(text="Daftar akun baru"),
            style="text",
            size_hint_y=None,
            height="40dp",
        )
        btn_daftar.bind(on_press=lambda x: setattr(self.manager, "current", "register"))

        btn_tamu = MDButton(
            MDButtonText(text="Masuk sebagai Tamu"),
            style="text",
            size_hint_y=None,
            height="40dp",
        )
        btn_tamu.bind(on_press=self._do_guest)

        layout.add_widget(lbl)
        layout.add_widget(self.field_user)
        layout.add_widget(self.field_pass)
        layout.add_widget(btn_masuk)
        layout.add_widget(btn_daftar)
        layout.add_widget(btn_tamu)
        self.add_widget(layout)

    def _do_login(self, *args):
        ok, msg = self.auth.login(self.field_user.text, self.field_pass.text)
        if ok:
            Snackbar(text=msg).open()
            self.manager.current = "dashboard"
        else:
            Snackbar(text=msg).open()

    def _do_guest(self, *args):
        ok, msg = self.auth.login_guest()
        if ok:
            Snackbar(text=msg).open()
            self.manager.current = "dashboard"
        else:
            Snackbar(text=msg).open()
