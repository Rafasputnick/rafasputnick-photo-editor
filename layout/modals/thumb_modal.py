import copy
import os

import PySimpleGUI as sg
from layout.windows.window import Window
from PIL import Image


class ThumbModal(Window):
    def __init__(self, image: Image, path: str):
        layout = [
            [
                sg.Text("Width:"),
                sg.Input(size=(10, 1), key="-WIDTH-", default_text="500"),
                sg.Text("Height:"),
                sg.Input(size=(10, 1), key="-HEIGHT-", default_text="500"),
                sg.Button("Export"),
            ]
        ]
        func_map = {"Export": self.save_thumb}
        super().__init__(layout, func_map)
        self.current_image = image
        self.path = path

    def start(self):
        super().start("Export as thumbnail", True)

    def add_path_suffix(self, suffix: str):
        filename, file_extension = os.path.splitext(self.path)
        if file_extension == "":
            file_extension = ".jpg"
        return filename + suffix + file_extension

    def save_thumb(self, value: dict):
        try:
            new_file = self.add_path_suffix("_thumb")
            temp_image = copy.deepcopy(self.current_image)
            width = int(value["-WIDTH-"])
            heigth = int(value["-HEIGHT-"])
            temp_image.thumbnail((width, heigth))
            temp_image.save(new_file)
            self.close()
        except:
            raise Exception("An error happened when save")
