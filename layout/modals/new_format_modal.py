import os

import PySimpleGUI as sg
from layout.windows.window import Window
from PIL import Image


class NewFormatModal(Window):
    def __init__(self, image: Image, path: str):
        layout = [
            [
                sg.Text("Format:"),
                sg.Combo(
                    ["JPEG", "PNG", "BMP", "GIF", "ICO"],
                    key="-FORMAT-",
                    default_value="JPEG",
                ),
                sg.Button("Export"),
            ]
        ]
        func_map = {"Export": self.save_new_format}
        super().__init__(layout, func_map)
        self.current_image = image
        self.path = path

    def start(self):
        super().start("Export in another format", True)

    def add_path_suffix(self, suffix: str):
        filename, file_extension = os.path.splitext(self.path)
        file_extension = file_extension if file_extension != "" else ".jpg"
        return filename + suffix + file_extension

    def save_new_format(self, value: dict):
        try:
            filename, file_extension = os.path.splitext(self.path)
            format = value["-FORMAT-"]
            filename += "." + str(format).lower()
            self.current_image.convert("RGB").save(filename, format=format)
            self.close()
        except:
            raise Exception("An error happened when save")
