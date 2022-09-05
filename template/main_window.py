import PySimpleGUI as sg

from template.modal.low_quality_modal import LowQualityModal
from template.modal.new_format_modal import NewFormatModal
from template.modal.thumb_modal import ThumbModal
from template.modal.upload_modal import UploadModal
from template.window import Window


class MainWindow(Window):
    def __init__(self):
        layout = [
            [
                sg.Menu(
                    [["File", ["Open", "Save", ["Thumb", "Low quality", "New format"]]]]
                )
            ],
            [sg.Image(key="-IMAGE-", expand_x=True, expand_y=True)],
        ]
        func_map = {
            "Open": self.load_image,
            "Thumb": self.save_thumb,
            "Low quality": self.save_low_quality,
            "New format": self.save_new_format,
        }
        super().__init__(layout, func_map)
        self.current_image = None
        self.path = None

    def start(self):
        super().start("Sputnick Photo Editor")

    def load_image(self, value: dict):
        modal = UploadModal()
        self.current_image, self.path, bio = modal.start()
        if self.current_image and self.path and bio:
            self.window["-IMAGE-"].update(data=bio.getvalue(), size=(500, 500))

    def save_thumb(self, value: dict):
        modal = ThumbModal(self.current_image, self.path)
        modal.start()

    def save_low_quality(self, value: dict):
        modal = LowQualityModal(self.current_image, self.path)
        modal.start()

    def save_new_format(self, value: dict):
        modal = NewFormatModal(self.current_image, self.path)
        modal.start()
