import PySimpleGUI as sg
from window import Window
from PIL import Image
import io
import os
import validators
import copy
import requests
import re

class MainWindow(Window):

    def __init__(self):
        layout = [
            [
                sg.Menu([["File",
                                ["Open",
                                 "Save",
                                        [
                                            "Thumb", "Low quality", "New format"
                                        ]
                                ]
                        ]])
            ],
            [sg.Image(key="-IMAGE-", size=(500,500))],
            [   sg.Text("Abrir imagem em:"), 
                sg.Input(size=(25,1), key="-FILE-"),
                sg.FileBrowse([("JPEG (*.jpg)", "*.jpg"), ("Todos os arquivos", "*")]),
                sg.Button("Carregar imagem")
            ],
            [
                sg.Button("Save Thumb"),
                sg.Button("Salvar com redução de qualidade"),
                sg.Text("Formato:"), 
                sg.Combo(["JPEG", "PNG", "BMP", "GIF"], key="-FORMAT-"),
                sg.Button("Salvar no formato novo")
            ],
            [
                sg.Text("Url:"),
                sg.Input(size=(75,1), key="-URL-"),
                sg.Button("Carregar imagem url")
            ]
        ]
        mapa_funcoes = {
                        "Open": self.load_image,
                        "Thumb": self.save_thumb,
                        "Low quality": self.save_low_quality,
                        "New format": self.save_new_format
                       }
        super().__init__(layout, mapa_funcoes)
        self.current_image = None
        self.path = None
    
    def start(self):
        return super().start("Sputnick Photo Editor", False)

    def add_path_suffix(self, suffix: str):
        filename, file_extension = os.path.splitext(self.path)
        return filename + suffix + file_extension

    def load_image(self, value: dict):

        self.path = value["-FILE-"]

        if validators.url(self.path):
            self.path = re.sub(r'^https', 'http', self.path)
            response = requests.get(self.path, verify=False)
            self.current_image = Image.open(io.BytesIO(response.content))

            match = re.match(r'.+\/([A-z-]+).*$', self.path)
            if match != None:
                self.path = match[1]
            else:
                self.path = "image"
        elif os.path.exists(self.path):
            self.current_image = Image.open(self.path)
            self.current_image.thumbnail((500,500))
        else:
            print("Não foi possivel abrir")
            return True
        
        bio = io.BytesIO()
        self.current_image.save(bio, format="PNG")
        self.window['-IMAGE-'].update(data=bio.getvalue(), size=(500,500))
        return True
    
    def save_thumb(self, value: dict):
        new_file = self.add_path_suffix('_thumb')
        temp_image = copy.deepcopy(self.current_image)
        temp_image.thumbnail((500,500))
        temp_image.save(new_file)
        return True

    def save_low_quality(self, value: dict):
        new_file = self.add_path_suffix('_downgrade')
        self.current_image.save(new_file, optimize=True, quality=70)
        return True

    def save_new_format(self, value: dict):
        filename, file_extension = os.path.splitext(self.path)
        format = value["-FORMAT-"]
        filename += '.' + str(format).lower()
        self.current_image.convert('RGB').save(filename, format=format)
        return True