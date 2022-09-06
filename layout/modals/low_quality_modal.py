import os

import PySimpleGUI as sg
from layout.windows.window import Window
from PIL import Image


class LowQualityModal(Window):
    def __init__(self, image: Image, path: str):
        layout = [
            [
                sg.Text("Quality (0% - 100%):"),
                sg.Input(size=(10, 1), key="-QUALITY-", default_text="70"),
                sg.Button("Export"),
            ]
        ]
        func_map = {"Export": self.save_low_quality}
        super().__init__(layout, func_map)
        self.current_image = image
        self.path = path

    def start(self):
        super().start("Export in a lower quality", True)

    def add_path_suffix(self, suffix: str):
        filename, file_extension = os.path.splitext(self.path)
        file_extension = file_extension if file_extension != "" else ".jpg"
        return filename + suffix + file_extension

    def save_low_quality(self, value: dict):
        try:
            new_file = self.add_path_suffix("_downgrade")
            quality = int(value["-QUALITY-"])
            self.current_image.save(new_file, optimize=True, quality=quality)
            self.close()
        except:
            raise Exception("An error happened when save")
