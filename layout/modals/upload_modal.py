import io
import os
import re

import PySimpleGUI as sg
import requests
import validators
from layout.windows.window import Window
from PIL import Image


class UploadModal(Window):
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
        self.path = None

    def start(self):
        super().start("Load image", True)
        return self.current_image, self.path

    def load_image(self, value: dict):

        self.path = value["-PATH-"]

        if validators.url(self.path):
            self.path = re.sub(r"^https", "http", self.path)
            response = requests.get(self.path, verify=False)
            self.current_image = Image.open(io.BytesIO(response.content))

            match = re.match(r".+\/([A-z-]+).*$", self.path)
            if match != None:
                self.path = match[1]
            else:
                self.path = "image"
        elif os.path.exists(self.path):
            self.current_image = Image.open(self.path)
        else:
            raise Exception("An error happened when open the image")

        self.close()
