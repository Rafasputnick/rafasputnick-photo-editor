import PySimpleGUI as sg
from layout.windows.window import Window


class EnhanceModal(Window):
    def __init__(self, input_text: str):
        layout = [
            [
                sg.Text("Choose the enhance factor:"),
            ],
            [
                sg.Text(input_text),
                sg.Input(size=(25, 1), key="-FACTOR-", default_text="0.0"),
            ],
            [
                sg.Button("Apply"),
            ],
        ]
        func_map_with_values = {"Apply": self.aply_change}
        func_map = {}
        super().__init__(layout, func_map_with_values, func_map)
        self.enhance_value = None

    def start(self):
        super().start("Set enhance", True)
        return self.enhance_value

    def aply_change(self, value: dict):
        self.enhance_value = float(value["-FACTOR-"])
        self.close()
