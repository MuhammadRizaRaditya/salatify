"""View Jadwal Sholat."""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import MDSnackbar as Snackbar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivy.clock import Clock
from utils.constants import COLOR_PRIMARY, COLOR_ACCENT, COLOR_TEXT, PRAYER_LABELS


class PrayerScreen(Screen):
    def __init__(self, prayer_controller, **kwargs):
        super().__init__(**kwargs)
        self.name = "prayer"
        self.ctrl = prayer_controller
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

        title = MDLabel(text="Jadwal Sholat", halign="left", theme_text_color="Custom",
                        text_color=COLOR_PRIMARY,             font_style="Title", bold=True,
                        size_hint_y=None, height="40dp")

        card = MDCard(size_hint_y=None, height="260dp", padding="15dp", radius=[16, 16, 16, 16])
        card.md_bg_color = "#FFFFFF"
        cbox = MDBoxLayout(orientation="vertical", spacing="8dp")
        ctitle = MDLabel(text="Jadwal Hari Ini", halign="left", theme_text_color="Custom",
                         text_color=COLOR_PRIMARY,             font_style="Title", bold=True,
                         size_hint_y=None, height="30dp")
        grid = MDGridLayout(cols=5, spacing="8dp", size_hint_y=None, height="160dp")
        self.widgets = {}
        for key in ["subuh", "dzuhur", "ashar", "maghrib", "isya"]:
            w = MDBoxLayout(orientation="vertical", size_hint_y=None, height="140dp")
            w.md_bg_color = "#F0F4F1"
            w.radius = [12, 12, 12, 12]
            lb = MDLabel(text=PRAYER_LABELS[key], halign="center", theme_text_color="Custom",
                         text_color=COLOR_TEXT,             font_style="Body", size_hint_y=None, height="20dp")
            lt = MDLabel(text="--:--", halign="center", theme_text_color="Custom",
                         text_color=COLOR_PRIMARY,             font_style="Title", bold=True, size_hint_y=None, height="30dp")
            lt2 = MDLabel(text="--:--", halign="center", theme_text_color="Custom",
                          text_color=COLOR_ACCENT,             font_style="Body", size_hint_y=None, height="24dp")
            w.add_widget(lb)
            w.add_widget(lt)
            w.add_widget(lt2)
            grid.add_widget(w)
            self.widgets[key] = (lt, lt2)

        cbox.add_widget(ctitle)
        cbox.add_widget(grid)
        card.add_widget(cbox)

        btn_refresh = MDButton(MDButtonText(text="Perbarui Jadwal"), style="filled",
                               size_hint_y=None, height="44dp")
        btn_refresh.bind(on_press=self._refresh)

        box.add_widget(title)
        box.add_widget(card)
        box.add_widget(btn_refresh)
        scroll.add_widget(box)
        self.root.add_widget(scroll)
        self._refresh()

    def _refresh(self, *args):
        pref = self.ctrl.get_preferences()
        lat = pref.latitude if pref else "-6.2"
        lon = pref.longitude if pref else "106.8"
        metode = pref.metode if pref else "mwml"
        from datetime import datetime
        tanggal = datetime.now().strftime("%Y-%m-%d")
        data = self.ctrl.ambil_jadwal(lat, lon, metode, tanggal)
        if data:
            for key in ["subuh", "dzuhur", "ashar", "maghrib", "isya"]:
                lt, lt2 = self.widgets[key]
                lt.text = data.get(key, "--:--")
                lt2.text = data.get(key, "--:--")
            Snackbar(text="Jadwal sholat diperbarui.").open()
        else:
            data = self.ctrl.jadwal_offline(tanggal)
            if data:
                for key in ["subuh", "dzuhur", "ashar", "maghrib", "isya"]:
                    lt, lt2 = self.widgets[key]
                    lt.text = data.get(key, "--:--")
                    lt2.text = data.get(key, "--:--")
                Snackbar(text="Menampilkan jadwal tersimpan (offline).").open()
            else:
                Snackbar(text="Gagal mengambil jadwal sholat. Coba lagi nanti.").open()
