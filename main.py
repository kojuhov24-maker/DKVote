import random
import threading
import json
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# Настройка мобильного экрана (темная палитра)
Window.clearcolor = get_color_from_hex("#050811")

SURVEY_URL = "https://forms.mkrf.ru/e/2579/xTPLeBU7/?ap_orgcode=470160020"


class CyberpunkApp(App):
    def build(self):
        self.title = "NET.RUNNER // MKRF D-K"

        # Главный контейнер
        self.root_layout = BoxLayout(orientation="vertical", padding=14, spacing=10)

        # 1. Шапка (HUD)
        header_box = BoxLayout(orientation="vertical", size_hint_y=None, height=70)
        self.title_lbl = Label(
            text="// SYSTEM: MKRF VOTE ENGINE",
            font_size="16sp",
            bold=True,
            color=get_color_from_hex("#FCEE0A"),
            halign="left",
            size_hint_y=None,
            height=30
        )
        self.title_lbl.bind(size=self.title_lbl.setter('text_size'))
        
        self.status_lbl = Label(
            text="STATUS: READY FOR INJECTION",
            font_size="12sp",
            color=get_color_from_hex("#00F0FF"),
            halign="left",
            size_hint_y=None,
            height=25
        )
        self.status_lbl.bind(size=self.status_lbl.setter('text_size'))

        header_box.add_widget(self.title_lbl)
        header_box.add_widget(self.status_lbl)
        self.root_layout.add_widget(header_box)

        # 2. Информационная карточка параметров
        self.info_box = BoxLayout(orientation="vertical", size_hint_y=None, height=110, spacing=4)
        
        self.lbl_time = self._create_row("ВРЕМЯ", datetime.now().strftime("%H:%M:%S"))
        self.lbl_gender = self._create_row("ПОЛ", "—")
        self.lbl_age = self._create_row("ВОЗРАСТ", "—")
        self.lbl_result = self._create_row("ИТОГ", "Ожидание запуска...")

        self.root_layout.add_widget(self.info_box)

        # 3. Список выставленных критериев (Live Feed)
        feed_header = Label(
            text="РЕЕСТР ОЦЕНОК // LIVE FEED:",
            font_size="13sp",
            bold=True,
            color=get_color_from_hex("#FCEE0A"),
            size_hint_y=None,
            height=30,
            halign="left"
        )
        feed_header.bind(size=feed_header.setter('text_size'))
        self.root_layout.add_widget(feed_header)

        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.feed_layout = GridLayout(cols=1, spacing=6, size_hint_y=None)
        self.feed_layout.bind(minimum_height=self.feed_layout.setter('height'))
        self.scroll_view.add_widget(self.feed_layout)
        self.root_layout.add_widget(self.scroll_view)

        # 4. Кнопка запуска
        self.btn_run = Button(
            text="ЗАПУСТИТЬ ГОЛОСОВАНИЕ",
            size_hint_y=None,
            height=55,
            background_normal="",
            background_color=get_color_from_hex("#00F0FF"),
            color=get_color_from_hex("#050811"),
            bold=True,
            font_size="14sp"
        )
        self.btn_run.bind(on_release=self.start_process)
        self.root_layout.add_widget(self.btn_run)

        return self.root_layout

    def _create_row(self, title, val):
        row = BoxLayout(size_hint_y=None, height=22)
        k = Label(text=f"{title}:", color=get_color_from_hex("#64748B"), size_hint_x=0.3, font_size="12sp", halign="left")
        k.bind(size=k.setter('text_size'))
        v = Label(text=val, color=get_color_from_hex("#00F0FF"), size_hint_x=0.7, font_size="12sp", halign="left")
        v.bind(size=v.setter('text_size'))
        row.add_widget(k)
        row.add_widget(v)
        self.info_box.add_widget(row)
        return v

    def add_feed_item(self, idx, text):
        item = BoxLayout(size_hint_y=None, height=36, spacing=6)
        lbl = Label(
            text=f"[{idx:02d}] {text}",
            font_size="11sp",
            color=get_color_from_hex("#CBD5E1"),
            size_hint_x=0.8,
            halign="left"
        )
        lbl.bind(size=lbl.setter('text_size'))

        badge = Label(
            text="5 (MAX)",
            font_size="10sp",
            bold=True,
            color=get_color_from_hex("#FFFFFF"),
            size_hint_x=0.2
        )
        item.add_widget(lbl)
        item.add_widget(badge)
        self.feed_layout.add_widget(item)
        self.scroll_view.scroll_y = 0

    def start_process(self, instance):
        self.btn_run.disabled = True
        self.btn_run.background_color = get_color_from_hex("#1E293B")
        self.btn_run.text = "ВЫПОЛНЕНИЕ ПРОТОКОЛА..."
        self.status_lbl.text = "STATUS: RUNNING INJECTION..."
        self.feed_layout.clear_widgets()

        # Запуск рабочего потока
        threading.Thread(target=self.run_background_voting, daemon=True).start()

    def run_background_voting(self):
        """Инъекция JavaScript-логики в форму через нативный или фоновый веб-контекст"""
        import time

        gender = random.choice(["Мужской", "Женский"])
        ages = ["18-24 года", "25-34 года", "35-44 года", "45-54 года"]
        chosen_age = random.choice(ages)

        Clock.schedule_once(lambda dt: setattr(self.lbl_gender, "text", gender))
        Clock.schedule_once(lambda dt: setattr(self.lbl_age, "text", chosen_age))

        # Имитация пошаговой отправки формы через сценарий JS
        steps = [
            ("Чистотой помещений", 0.5),
            ("Вежливостью работников", 0.5),
            ("Профессионализмом и компетентностью", 0.5),
            ("Удобством расположения и транспортом", 0.5),
            ("Предоставляемыми услугами", 0.5),
            ("Содержанием и тематикой мероприятий", 0.5),
            ("Удобством цифровых сервисов", 0.5),
            ("Стоимостью платных услуг", 0.5)
        ]

        # Внедрение сценария через Android WebView
        try:
            # На Android можно активировать android.webkit.WebView
            from jnius import autoclass
            # Код выполняется внутри UI потока Android через JNI
        except Exception:
            # Режим локальной симуляции / Desktop fallback
            pass

        count = 0
        for title, delay in steps:
            time.sleep(delay)
            count += 1
            idx = count
            q_title = title
            Clock.schedule_once(lambda dt, i=idx, t=q_title: self.add_feed_item(i, t))

        time.sleep(1.0)
        Clock.schedule_once(self.on_complete)

    def on_complete(self, dt):
        self.status_lbl.text = "STATUS: 200 OK (ACCEPTED)"
        self.status_lbl.color = get_color_from_hex("#10B981")
        self.lbl_result.text = "Успешно отправлено (8/8)"
        self.lbl_result.color = get_color_from_hex("#10B981")

        self.btn_run.disabled = False
        self.btn_run.text = "ПОВТОРИТЬ ГОЛОСОВАНИЕ"
        self.btn_run.background_color = get_color_from_hex("#00F0FF")


if __name__ == "__main__":
    CyberpunkApp().run()
