import PySimpleGUI as sg
from layout.windows.window import Window


class RotateModal(Window):
    def __init__(self):
        layout = [
            [
                sg.Text("Choose the rotation value:"),
            ],
            [
                sg.Text("Degrees:"),
                sg.Input(size=(25, 1), key="-DEGREES-", default_text="0"),
            ],
            [
                sg.Button("Apply"),
            ],
        ]
        func_map_with_values = {"Apply": self.aply_change}
        func_map = {}
        super().__init__(layout, func_map_with_values, func_map)
        self.rotate_value = None

    def start(self):
        super().start("Set rotation", True)
        return self.rotate_value

    def aply_change(self, value: dict):
        self.rotate_value = int(value["-DEGREES-"])
        self.close()
