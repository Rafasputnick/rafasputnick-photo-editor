import io
import os
import re

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
        func_map = {"Import": self.load_image}
        super().__init__(layout, func_map)
        self.current_image = None

    def start(self):
        super().start("Load image", True)
        return self.current_image

    def load_image(self, value: dict):

        path = value["-PATH-"]

        if validators.url(path):
            path = re.sub(r"^https", "http", path)
            response = requests.get(path, verify=False)
            self.current_image = Image.open(io.BytesIO(response.content))

            match = re.match(r".+\/([A-z-]+).*$", path)
            if match != None:
                path = match[1]
            else:
                path = "image"
        elif os.path.exists(path):
            self.current_image = Image.open(path)
        else:
            raise Exception("An error happened when open the image")

        self.close()
