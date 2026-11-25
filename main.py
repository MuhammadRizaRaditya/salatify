"""Titik masuk aplikasi SALATIFY."""

import os
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp

from database.db import init_db, get_session
from controllers.auth_controller import AuthController
from controllers.dashboard_controller import DashboardController
from controllers.prayer_controller import PrayerController
from controllers.qibla_controller import QiblaController
from controllers.dzikir_controller import DzikirController
from controllers.doa_controller import DoaController
from controllers.quran_controller import QuranController
from services.location_service import LocationService
from services.notification_service import NotificationService
from services.audio_service import AudioService
from views.splash_screen import SplashScreen
from views.login_screen import LoginScreen
from views.register_screen import RegisterScreen
from views.dashboard_screen import DashboardScreen
from views.prayer_screen import PrayerScreen
from views.qibla_screen import QiblaScreen
from views.dzikir_screen import DzikirScreen
from views.doa_screen import DoaScreen
from views.doa_detail_screen import DoaDetailScreen
from views.quran_screen import QuranScreen
from views.settings_screen import SettingsScreen
from utils.constants import COLOR_PRIMARY, COLOR_BACKGROUND, COLOR_TEXT


class SalatifyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "SALATIFY"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "800"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Light"

        self.app_data_dir = os.path.abspath(self.user_data_dir)
        init_db(self.app_data_dir)

        self.auth = AuthController(self.app_data_dir)
        self.session = get_session()

        self.location = LocationService()
        self.notification = NotificationService()
        self.audio = AudioService()

        self.dashboard = DashboardController(user_id=None, timezone_str="Asia/Jakarta")
        self.prayer = PrayerController(user_id=None)
        self.qibla = QiblaController()
        self.dzikir = DzikirController(user_id=None)
        self.doa = DoaController(user_id=None)
        self.quran = QuranController(user_id=None, audio_service=self.audio)

        Window.clearcolor = (0.945, 0.957, 0.941, 1)  # #F1F4F5-ish
        Window.softinput_mode = "below_target"

    def build(self):
        sm = ScreenManager(transition=NoTransition())

        sm.add_widget(SplashScreen())
        sm.add_widget(LoginScreen(auth_controller=self.auth))
        sm.add_widget(RegisterScreen(auth_controller=self.auth))
        sm.add_widget(DashboardScreen(dashboard_controller=self.dashboard))
        sm.add_widget(PrayerScreen(prayer_controller=self.prayer))
        sm.add_widget(QiblaScreen(qibla_controller=self.qibla, location_service=self.location))
        sm.add_widget(DzikirScreen(dzikir_controller=self.dzikir))
        sm.add_widget(DoaScreen(doa_controller=self.doa))
        sm.add_widget(DoaDetailScreen(doa_controller=self.doa))
        sm.add_widget(QuranScreen(quran_controller=self.quran, audio_service=self.audio))
        sm.add_widget(SettingsScreen(auth_controller=self.auth))

        return sm

    def on_start(self):
        self.root.current = "splash"


if __name__ == "__main__":
    SalatifyApp().run()
