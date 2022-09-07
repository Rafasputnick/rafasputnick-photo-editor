import PySimpleGUI as sg
from layout.windows.window import Window
from PIL import Image


class ExportModal(Window):
    def __init__(self, image: Image, filename: str):
        if not image:
            raise Exception("Image not found")
        width, height = image.size
        layout = [
            [
                sg.Text("Filename:"),
                sg.Input(size=(10, 1), key="-FILENAME-", default_text=filename),
            ],
            [
                sg.Text("Width:"),
                sg.Input(size=(10, 1), key="-WIDTH-", default_text=str(width)),
                sg.Text("Height:"),
                sg.Input(size=(10, 1), key="-HEIGHT-", default_text=str(height)),
            ],
            [
                sg.Text("Quality (0% - 100%):"),
                sg.Input(size=(10, 1), key="-QUALITY-", default_text="100"),
            ],
            [
                sg.Text("Format:"),
                sg.Combo(
                    ["JPEG", "PNG", "BMP", "GIF", "ICO"],
                    key="-FORMAT-",
                    default_value="JPEG",
                ),
            ],
            [sg.Button("Export")],
        ]
        func_map = {"Export": self.export}
        super().__init__(layout, func_map)
        self.current_image = image
        self.filename = filename

    def start(self):
        super().start("Export image", True)
        return self.current_image, self.filename

    def export(self, value: dict):
        try:
            quality = int(value["-QUALITY-"])
            format = str(value["-FORMAT-"]).lower()
            self.filename = value["-FILENAME-"]
            path = "exports/" + self.filename + "." + format
            width = int(value["-WIDTH-"])
            heigth = int(value["-HEIGHT-"])
            size = width, heigth
            self.current_image.thumbnail(size, Image.ANTIALIAS)
            self.current_image.save(path, optimize=True, quality=quality, format=format)
            self.close()
        except:
            raise Exception("An error happened when save")
