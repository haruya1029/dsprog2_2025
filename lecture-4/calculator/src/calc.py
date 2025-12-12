import flet as ft
import math


class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text


class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.Colors.WHITE24
        self.color = ft.Colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.Colors.ORANGE
        self.color = ft.Colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.Colors.BLUE_GREY_100
        self.color = ft.Colors.BLACK


class SciButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.Colors.GREEN_200
        self.color = ft.Colors.BLACK


class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=20)
        self.width = 350
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20

        # 科学計算ボタン（5つ以上）: sin, cos, tan, log, exp
        sci_row = ft.Row(
            controls=[
                SciButton(text="sin", button_clicked=self.button_clicked),
                SciButton(text="cos", button_clicked=self.button_clicked),
                SciButton(text="tan", button_clicked=self.button_clicked),
                SciButton(text="log", button_clicked=self.button_clicked),
                SciButton(text="exp", button_clicked=self.button_clicked),
            ],
            alignment="spaceBetween",
        )

        # 通常ボタン
        normal_rows = [
            ft.Row(
                controls=[
                    ExtraActionButton(text="AC", button_clicked=self.button_clicked),
                    ExtraActionButton(text="+/-", button_clicked=self.button_clicked),
                    ExtraActionButton(text="%", button_clicked=self.button_clicked),
                    ActionButton(text="/", button_clicked=self.button_clicked),
                ]
            ),
            ft.Row(
                controls=[
                    DigitButton(text="7", button_clicked=self.button_clicked),
                    DigitButton(text="8", button_clicked=self.button_clicked),
                    DigitButton(text="9", button_clicked=self.button_clicked),
                    ActionButton(text="*", button_clicked=self.button_clicked),
                ]
            ),
            ft.Row(
                controls=[
                    DigitButton(text="4", button_clicked=self.button_clicked),
                    DigitButton(text="5", button_clicked=self.button_clicked),
                    DigitButton(text="6", button_clicked=self.button_clicked),
                    ActionButton(text="-", button_clicked=self.button_clicked),
                ]
            ),
            ft.Row(
                controls=[
                    DigitButton(text="1", button_clicked=self.button_clicked),
                    DigitButton(text="2", button_clicked=self.button_clicked),
                    DigitButton(text="3", button_clicked=self.button_clicked),
                    ActionButton(text="+", button_clicked=self.button_clicked),
                ]
            ),
            ft.Row(
                controls=[
                    DigitButton(text="0", expand=2, button_clicked=self.button_clicked),
                    DigitButton(text=".", button_clicked=self.button_clicked),
                    ActionButton(text="=", button_clicked=self.button_clicked),
                ]
            ),
        ]

        self.content = ft.Column(
            controls=[ft.Row(controls=[self.result], alignment="end"), sci_row] + normal_rows
        )

    def button_clicked(self, e):
        data = e.control.data

        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()
            self.update()
            return

        # 数字と小数点
        if data in "0123456789.":
            if self.result.value == "0" or self.new_operand:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value += data

        # 四則演算
        elif data in ("+", "-", "*", "/"):
            self.result.value = self.calculate(self.operand1, float(self.result.value), self.operator)
            self.operator = data
            self.operand1 = 0 if self.result.value == "Error" else float(self.result.value)
            self.new_operand = True

        # =
        elif data == "=":
            self.result.value = self.calculate(self.operand1, float(self.result.value), self.operator)
            self.reset()

        # %
        elif data == "%":
            self.result.value = float(self.result.value) / 100
            self.reset()

        # +/-
        elif data == "+/-":
            num = float(self.result.value)
            self.result.value = str(self.format_number(-num))

        #
        elif data == "sin":
            self.result.value = str(self.format_number(math.sin(math.radians(float(self.result.value)))))
            self.reset()

        elif data == "cos":
            self.result.value = str(self.format_number(math.cos(math.radians(float(self.result.value)))))
            self.reset()

        elif data == "tan":
            self.result.value = str(self.format_number(math.tan(math.radians(float(self.result.value)))))
            self.reset()

        elif data == "log":  # 自然対数
            try:
                self.result.value = str(self.format_number(math.log(float(self.result.value))))
            except:
                self.result.value = "Error"
            self.reset()

        elif data == "exp":
            self.result.value = str(self.format_number(math.exp(float(self.result.value))))
            self.reset()

        self.update()

    def format_number(self, num):
        return int(num) if num % 1 == 0 else num

    def calculate(self, operand1, operand2, operator):
        try:
            if operator == "+":
                return self.format_number(operand1 + operand2)
            if operator == "-":
                return self.format_number(operand1 - operand2)
            if operator == "*":
                return self.format_number(operand1 * operand2)
            if operator == "/":
                if operand2 == 0:
                    return "Error"
                return self.format_number(operand1 / operand2)
        except:
            return "Error"

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Scientific Calculator"
    calc = CalculatorApp()
    page.add(calc)


ft.app(main)
