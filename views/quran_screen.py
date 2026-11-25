"""View Al-Qur'an dan Murottal: daftar surah + layar detail pemutar audio."""

from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import MDSnackbar as Snackbar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.slider import MDSlider
from kivymd.uix.progressbar import MDProgressBar
from kivy.clock import Clock
from utils.constants import COLOR_PRIMARY, COLOR_ACCENT, COLOR_TEXT


class QuranScreen(Screen):
    def __init__(self, quran_controller, audio_service, **kwargs):
        super().__init__(**kwargs)
        self.name = "quran"
        self.ctrl = quran_controller
        self.audio = audio_service
        self._surat_terpilih = None
        self._progress_event = None
        self._detail_box = None
        self._status_label = None
        self._vol_slider = None
        self._progress_bar = None
        self._play_btn = None
        self._dl_indicator = None
        self._build_ui()

    def _build_ui(self):
        self.root = MDBoxLayout(orientation="vertical")
        self.root.md_bg_color = "#F7F8F5"
        self.add_widget(self.root)

    def on_enter(self, *args):
        self.root.clear_widgets()
        self._show_list()

    def on_pre_leave(self, *args):
        self._stop_progress()
        self.ctrl.stop_surah()

    # ---------- list ----------
    def _show_list(self):
        self.root.clear_widgets()
        self._detail_box = None
        scroll = MDScrollView()
        box = MDBoxLayout(orientation="vertical", spacing="12dp", padding="16dp",
                          size_hint_y=None, height="900dp")
        box.md_bg_color = "#F7F8F5"

        title = MDLabel(text="Al-Qur'an", halign="left", theme_text_color="Custom",
                        text_color=COLOR_PRIMARY, font_style="Headline", bold=True,
                        size_hint_y=None, height="40dp")

        self.field_cari = MDTextField(hint_text="Cari surah...", mode="filled",
                                      size_hint_y=None, height="48dp")
        self.field_cari.bind(text=self._on_cari)

        self.daftar_box = MDBoxLayout(orientation="vertical", spacing="8dp",
                                      size_hint_y=None, height="650dp")

        box.add_widget(title)
        box.add_widget(self.field_cari)
        box.add_widget(self.daftar_box)
        scroll.add_widget(box)
        self.root.add_widget(scroll)
        self._load_surah()

    def _on_cari(self, instance, value):
        self._load_surah(q=value)

    def _load_surah(self, q=None):
        self.daftar_box.clear_widgets()
        daftar = self.ctrl.daftar_surah(q=q)
        if not daftar:
            self.daftar_box.add_widget(MDLabel(text="Surah tidak ditemukan.",
                                               halign="center", theme_text_color="Custom",
                                               text_color=COLOR_TEXT, size_hint_y=None, height="40dp"))
            return
        for s in daftar:
            card = MDCard(size_hint_y=None, height="72dp", padding="10dp", radius=[12, 12, 12, 12])
            card.md_bg_color = "#FFFFFF"
            w = MDBoxLayout(orientation="vertical", spacing="2dp")
            w1 = MDLabel(text=f"{s.nomor}. {s.nama_latin}", halign="left", theme_text_color="Custom",
                         text_color=COLOR_PRIMARY, font_style="Title", bold=True,
                         size_hint_y=None, height="22dp")
            status_txt = "Tersedia offline" if self.ctrl.is_downloaded(s.nomor) else "Belum diunduh"
            w2 = MDLabel(text=f"{s.nama_arab} • {s.jumlah_ayat} ayat • {s.jenis}   [{status_txt}]",
                         halign="left", theme_text_color="Custom",
                         text_color=COLOR_TEXT, font_style="Label", size_hint_y=None, height="18dp")
            w.add_widget(w1)
            w.add_widget(w2)
            card.add_widget(w)

            btn_box = MDBoxLayout(size_hint_x=None, width="90dp", spacing="5dp")
            btn_play = MDButton(style="eased", size_hint=(None, None), size=("40dp", "36dp"))
            btn_play.add_widget(MDButtonText(text="Play"))
            btn_play.bind(on_press=lambda x, nomor=s.nomor: self._pilih_surah(nomor))
            btn_box.add_widget(btn_play)
            card.add_widget(btn_box)

            card.bind(on_press=lambda x, nomor=s.nomor: self._pilih_surah(nomor))
            self.daftar_box.add_widget(card)

    def _pilih_surah(self, nomor_surah: int):
        s = self.ctrl.detail_by_nomor(nomor_surah)
        if not s:
            Snackbar(text="Data surah tidak tersedia.").open()
            return
        self._surat_terpilih = s
        self._show_detail()

    # ---------- detail ----------
    def _show_detail(self):
        self.root.clear_widgets()
        self._detail_box = MDBoxLayout(orientation="vertical", spacing="12dp",
                                       padding="16dp", size_hint_y=None, height="700dp")
        self._detail_box.md_bg_color = "#F7F8F5"

        s = self._surat_terpilih
        back = MDButton(style="text", size_hint=(None, None), size=("100dp", "36dp"))
        back.add_widget(MDButtonText(text="Kembali"))
        back.bind(on_press=lambda x: self._show_list())

        title = MDLabel(text=f"{s.nomor}. {s.nama_latin}", halign="left", theme_text_color="Custom",
                        text_color=COLOR_PRIMARY, font_style="Headline", bold=True,
                        size_hint_y=None, height="40dp")
        subtitle = MDLabel(text=f"{s.nama_arab} • {s.jumlah_ayat} ayat • {s.jenis}",
                           halign="left", theme_text_color="Custom",
                           text_color=COLOR_TEXT, font_style="Body2", size_hint_y=None, height="24dp")

        self._dl_indicator = MDLabel(text="Tersedia offline" if self.ctrl.is_downloaded(s.nomor)
                                     else "Belum diunduh",
                                     halign="left", theme_text_color="Custom",
                                     text_color=COLOR_ACCENT, font_style="Caption",
                                     size_hint_y=None, height="18dp")

        self._status_label = MDLabel(text="Siap", halign="left", theme_text_color="Custom",
                                     text_color=COLOR_TEXT, font_style="Caption",
                                     size_hint_y=None, height="18dp")

        # Kontrol pemutaran
        ctrl_box = MDBoxLayout(orientation="vertical", spacing="10dp", size_hint_y=None, height="220dp")

        btn_box = MDBoxLayout(spacing="10dp", size_hint_y=None, height="44dp")
        self._play_btn = MDButton(style="eased", size_hint=(None, None), size=("100dp", "40dp"))
        self._play_btn.add_widget(MDButtonText(text="Play"))
        self._play_btn.bind(on_press=self._toggle_play)
        btn_stop = MDButton(style="eased", size_hint=(None, None), size=("90dp", "40dp"))
        btn_stop.add_widget(MDButtonText(text="Stop"))
        btn_stop.bind(on_press=lambda x: self._stop())
        btn_box.add_widget(self._play_btn)
        btn_box.add_widget(btn_stop)

        vol_box = MDBoxLayout(size_hint_y=None, height="40dp")
        vol_lbl = MDLabel(text="Volume", halign="left", size_hint_x=None, width="60dp",
                          theme_text_color="Custom", text_color=COLOR_TEXT,
                          font_style="Caption", size_hint_y=None, height="40dp")
        self._vol_slider = MDSlider(min=0, max=1, value=self.ctrl.audio.volume,
                                    size_hint_x=1)
        self._vol_slider.bind(value=self._on_volume)
        vol_box.add_widget(vol_lbl)
        vol_box.add_widget(self._vol_slider)

        self._progress_bar = MDProgressBar(value=0, size_hint_y=None, height="6dp")
        prog_box = MDBoxLayout(size_hint_y=None, height="30dp")
        self._prog_now = MDLabel(text="0:00", halign="left", size_hint_x=None, width="40dp",
                                 theme_text_color="Custom", text_color=COLOR_TEXT,
                                 font_style="Caption", size_hint_y=None, height="30dp")
        self._prog_total = MDLabel(text="0:00", halign="right", size_hint_x=None, width="40dp",
                                   theme_text_color="Custom", text_color=COLOR_TEXT,
                                   font_style="Caption", size_hint_y=None, height="30dp")
        prog_box.add_widget(self._prog_now)
        prog_box.add_widget(self._progress_bar)
        prog_box.add_widget(self._prog_total)

        ctrl_box.add_widget(btn_box)
        ctrl_box.add_widget(vol_box)
        ctrl_box.add_widget(prog_box)

        tombol_unduh = MDButton(style="eased", size_hint=(None, None), size=("150dp", "40dp"))
        tombol_unduh.add_widget(MDButtonText(text="Unduh audio"))
        tombol_unduh.bind(on_press=lambda x: self._unduh(s.nomor))

        self._detail_box.add_widget(back)
        self._detail_box.add_widget(title)
        self._detail_box.add_widget(subtitle)
        self._detail_box.add_widget(self._dl_indicator)
        self._detail_box.add_widget(self._status_label)
        self._detail_box.add_widget(ctrl_box)
        self._detail_box.add_widget(tombol_unduh)

        self.root.add_widget(self._detail_box)

        # Daftarkan listener status audio.
        self.ctrl.add_listener(self._on_audio_status)
        self._update_play_button()
        self._start_progress()

    def _on_audio_status(self, status, error):
        self._status_label.text = status
        if error:
            Snackbar(text=error).open()
        self._update_play_button()
        if status in ("dihentikan", "gagal", "selesai"):
            self._stop_progress()

    def _update_play_button(self):
        if not self._play_btn:
            return
        if self.ctrl.playing:
            self._play_btn.children[0].text = "Pause"
        else:
            self._play_btn.children[0].text = "Play"

    def _toggle_play(self, *args):
        if not self._surat_terpilih:
            return
        if self.ctrl.playing:
            self.ctrl.pause_surah()
        else:
            self.ctrl.play_surah(self._surat_terpilih.nomor)

    def _stop(self, *args):
        self.ctrl.stop_surah()

    def _unduh(self, nomor_surah: int):
        self.ctrl.download_audio(nomor_surah)
        self._dl_indicator.text = "Mengunduh..."
        self._status_label.text = "mengunduh..."

    def _on_volume(self, instance, value):
        self.ctrl.set_volume(value)

    def _format_waktu(self, detik):
        menit = int(detik) // 60
        detik_detik = int(detik) % 60
        return f"{menit}:{detik_detik:02d}"

    def _start_progress(self):
        self._stop_progress()
        self._progress_event = Clock.schedule_interval(self._tick_progress, 0.5)

    def _stop_progress(self):
        if self._progress_event:
            self._progress_event.cancel()
            self._progress_event = None

    def _tick_progress(self, dt):
        if not self.ctrl.playing:
            self._stop_progress()
            return
        posisi, durasi = self.ctrl.progress()
        if durasi > 0:
            self._progress_bar.value = (posisi / durasi) * 100
        else:
            self._progress_bar.value = 0
        self._prog_now.text = self._format_waktu(posisi)
        self._prog_total.text = self._format_waktu(durasi)
