import PySimpleGUI as sg
from layout.windows.window import Window


class CustomFilterModal(Window):
    def __init__(self):
        layout = [
            [
                sg.Text("Choose the new white color:"),
            ],
            [
                sg.Text("Red:"),
                sg.Input(size=(25, 1), key="-RED-", default_text="0"),
            ],
            [
                sg.Text("Green:"),
                sg.Input(size=(25, 1), key="-GREEN-", default_text="0"),
            ],
            [
                sg.Text("Blue:"),
                sg.Input(size=(25, 1), key="-BLUE-", default_text="0"),
            ],
            [
                sg.Button("Apply"),
            ],
        ]
        func_map_with_values = {"Apply": self.aply_custom_white_filter}
        func_map = {}
        super().__init__(layout, func_map_with_values, func_map)
        self.new_white = None

    def start(self):
        super().start("Set new white", True)
        return self.new_white

    def aply_custom_white_filter(self, value: dict):
        red = int(value["-RED-"])
        green = int(value["-GREEN-"])
        blue = int(value["-BLUE-"])
        self.new_white = tuple((red, green, blue))
        self.close()
