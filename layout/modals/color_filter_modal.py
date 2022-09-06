import PySimpleGUI as sg
from filters.color_filter import ColorFilter
from layout.windows.window import Window
from PIL import Image


class ColorFilterModal(Window):
    def __init__(self, image: Image):
        layout = [
            [
                sg.Text("Choose how many color:"),
                sg.Input(size=(25, 1), key="-COLOR_NUM-", default_text="0"),
            ],
            [
                sg.Button("Apply"),
            ],
        ]
        func_map = {"Apply": self.aply_custom_white_filter}
        super().__init__(layout, func_map)
        self.current_image = image

    def start(self):
        super().start("Set new white", True)
        return self.current_image

    def aply_custom_white_filter(self, value: dict):
        colors_number = int(value["-COLOR_NUM-"])
        self.current_image = ColorFilter().apply(self.current_image, colors_number)
        self.close()
