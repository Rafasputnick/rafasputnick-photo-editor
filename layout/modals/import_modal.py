import io
import os
from pathlib import Path

import PySimpleGUI as sg
import requests
import validators
from layout.windows.window import Window
from PIL import Image


class ImportModal(Window):
    def __init__(self):
        layout = [
            [
                sg.Text("Choose path or url:"),
                sg.Input(size=(25, 1), key="-PATH-"),
                sg.FileBrowse(
                    button_text="Browse",
                    file_types=[("JPEG (*.jpg)", "*.jpg"), ("Todos os arquivos", "*")],
                ),
                sg.Button("Import"),
            ]
        ]
        func_map_with_value = {"Import": self.load_image}
        func_map = {}
        super().__init__(layout, func_map_with_value, func_map)
        self.current_image = None
        self.filename = None

    def start(self):
        super().start("Import image", True)
        return self.current_image, self.filename

    def load_image(self, value: dict):

        path = value["-PATH-"]

        if validators.url(path):
            response = requests.get(path, verify=False)
            self.current_image = Image.open(io.BytesIO(response.content))
            # self.current_image.thumbnail((500, 500))
            self.filename = "Untitled"
        elif os.path.exists(path):
            self.current_image = Image.open(path)
            self.filename = Path(path).stem
        else:
            raise Exception("An error happened when import the image")

        self.close()
