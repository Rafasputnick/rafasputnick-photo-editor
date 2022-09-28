import PySimpleGUI as sg
from layout.windows.window import Window


class ColorFilterModal(Window):
    def __init__(self):
        layout = [
            [
                sg.Text("Choose how many color:"),
                sg.Input(size=(25, 1), key="-COLOR_NUM-", default_text="0"),
            ],
            [
                sg.Button("Apply"),
            ],
        ]
        func_map = {}
        func_map_with_values = {"Apply": self.aply_custom_white_filter}
        super().__init__(layout, func_map_with_values, func_map)
        self.colors_number = None

    def start(self):
        super().start("Set the spec", True)
        return self.colors_number

    def aply_custom_white_filter(self, value: dict):
        self.colors_number = int(value["-COLOR_NUM-"])
        self.close()
