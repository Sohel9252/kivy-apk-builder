from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.core.window import Window

Window.clearcolor = (0.03, 0.04, 0.08, 1)


# ===== ODDS CONTROL =====
class OddsControl(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height=50, spacing=6, **kwargs)

        self.value = 1.67

        odds_list = [f"{x/100:.2f}" for x in range(150, 501)]

        self.spinner = Spinner(
            text=str(self.value),
            values=odds_list,
            size_hint_x=0.35,
            background_color=(0.12, 0.14, 0.2, 1),
            color=(1, 1, 1, 1)
        )

        self.input = TextInput(
            text=str(self.value),
            multiline=False,
            input_filter='float',
            size_hint_x=0.35,
            background_color=(0.08, 0.1, 0.16, 1),
            foreground_color=(0.9, 0.9, 0.9, 1)
        )

        self.minus = Button(text="-", size_hint_x=0.15,
                            background_color=(0.15, 0.18, 0.3, 1),
                            color=(1, 1, 1, 1))

        self.plus = Button(text="+", size_hint_x=0.15,
                           background_color=(0.15, 0.18, 0.3, 1),
                           color=(1, 1, 1, 1))

        self.minus.bind(on_press=self.dec)
        self.plus.bind(on_press=self.inc)

        self.spinner.bind(text=self.select_odds)
        self.input.bind(text=self.manual)

        self.add_widget(self.spinner)
        self.add_widget(self.input)
        self.add_widget(self.minus)
        self.add_widget(self.plus)

    def select_odds(self, instance, value):
        self.value = float(value)
        self.input.text = value

    def manual(self, instance, value):
        try:
            self.value = float(value)
        except:
            pass

    def inc(self, instance):
        self.value = round(self.value + 0.01, 2)
        self.sync()

    def dec(self, instance):
        if self.value > 1.01:
            self.value = round(self.value - 0.01, 2)
        self.sync()

    def sync(self):
        self.input.text = str(self.value)
        self.spinner.text = str(self.value)


# ===== MAIN APP =====
class BetAIPro(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=12, spacing=10, **kwargs)

        # ===== HEADER (BRAND STYLE) =====
        self.title = Label(
            text="SR BET AI PRO",
            font_size=26,
            bold=True,
            color=(0.2, 0.8, 1, 1),
            size_hint_y=None,
            height=40
        )

        self.subtitle = Label(
            text="Smart Betting Intelligence Engine",
            font_size=13,
            color=(0.6, 0.6, 0.7, 1),
            size_hint_y=None,
            height=25
        )

        # ===== INPUT FIELDS =====
        self.t1 = TextInput(
            hint_text="Team 1",
            background_color=(0.08, 0.1, 0.16, 1),
            foreground_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=50
        )

        self.o1 = OddsControl()

        self.t2 = TextInput(
            hint_text="Team 2",
            background_color=(0.08, 0.1, 0.16, 1),
            foreground_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=50
        )

        self.o2 = OddsControl()

        self.amount = TextInput(
            hint_text="Total Amount",
            input_filter='float',
            size_hint_y=None,
            height=50,
            background_color=(0.08, 0.1, 0.16, 1),
            foreground_color=(1, 1, 1, 1)
        )

        self.extra = TextInput(
            hint_text="Extra Bet (Optional)",
            input_filter='float',
            size_hint_y=None,
            height=50,
            background_color=(0.08, 0.1, 0.16, 1),
            foreground_color=(1, 1, 1, 1)
        )

        # ===== OUTPUT =====
        self.signal = Label(
            text="LIVE WAITING...",
            font_size=18,
            bold=True,
            size_hint_y=None,
            height=40
        )

        self.summary = Label(
            text="",
            size_hint_y=None,
            height=60,
            color=(0.8, 0.8, 0.8, 1)
        )

        self.details = Label(
            text="",
            size_hint_y=None,
            height=200,
            color=(0.7, 0.7, 0.7, 1),
            halign="left",
            valign="top"
        )

        self.details.bind(size=self.details.setter("text_size"))

        # ===== ADD UI =====
        self.add_widget(self.title)
        self.add_widget(self.subtitle)

        self.add_widget(self.t1)
        self.add_widget(self.o1)

        self.add_widget(self.t2)
        self.add_widget(self.o2)

        self.add_widget(self.amount)
        self.add_widget(self.extra)

        self.add_widget(self.signal)
        self.add_widget(self.summary)
        self.add_widget(self.details)

        # LIVE UPDATE
        self.amount.bind(text=self.calculate)
        self.extra.bind(text=self.calculate)
        self.t1.bind(text=self.calculate)
        self.t2.bind(text=self.calculate)
        self.o1.input.bind(text=self.calculate)
        self.o2.input.bind(text=self.calculate)

    # ===== ENGINE =====
    def calculate(self, *args):
        try:
            t1 = self.t1.text or "Team 1"
            t2 = self.t2.text or "Team 2"

            o1 = float(self.o1.value)
            o2 = float(self.o2.value)
            T = float(self.amount.text)

            extra = float(self.extra.text) if self.extra.text else 0

            if o1 <= 1 or o2 <= 1:
                return

            bet1 = (T * o2) / (o1 + o2)
            bet2 = (T * o1) / (o1 + o2)

            bet2 += extra
            T += extra

            r1 = bet1 * o1
            r2 = bet2 * o2

            min_r = min(r1, r2)
            loss = T - min_r
            arb = (1/o1) + (1/o2)

            if arb < 1:
                signal = "PROFIT MODE 🟢"
                color = (0.2, 0.9, 0.4, 1)
            elif abs(arb - 1) < 0.01:
                signal = "BREAK EVEN 🟡"
                color = (1, 0.85, 0.2, 1)
            else:
                signal = "EQUAL LOSS 🔴"
                color = (1, 0.3, 0.3, 1)

            self.signal.text = signal
            self.signal.color = color

            self.summary.text = f"{t1}: {round(bet1)} | {t2}: {round(bet2)}"

            self.details.text = f"""
TOTAL INVEST → {round(T)}

{t1} → {round(bet1)}
{t2} → {round(bet2)}

RETURN → {round(min_r)}
LOSS → {round(loss)}

MODE → {signal}
"""

        except:
            self.signal.text = "Waiting Input..."
            self.summary.text = ""
            self.details.text = ""


class BetApp(App):
    def build(self):
        return BetAIPro()


if __name__ == "__main__":
    BetApp().run()