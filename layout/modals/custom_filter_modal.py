import PySimpleGUI as sg
from filters.custom_white_filter import CustomWhiteFilter
from layout.windows.window import Window
from PIL import Image


class CustomFilterModal(Window):
    def __init__(self, image: Image):
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
            ]
        ]
        func_map = {"Apply": self.aply_custom_white_filter}
        super().__init__(layout, func_map)
        self.current_image = image

    def start(self):
        super().start("Set new white", True)
        return self.current_image

    def aply_custom_white_filter(self, value: dict):
        red = int(value["-RED-"])
        green = int(value["-GREEN-"])
        blue = int(value["-BLUE-"])
        new_white = tuple((red, green, blue))
        self.current_image = CustomWhiteFilter(new_white).apply(self.current_image)
        self.close()
