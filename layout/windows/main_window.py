import PySimpleGUI as sg
from filters.bw_filter import BwFilter
from filters.sepia_filter import SepiaFilter
from layout.modals.color_filter_modal import ColorFilterModal
from layout.modals.custom_filter_modal import CustomFilterModal
from layout.modals.low_quality_modal import LowQualityModal
from layout.modals.new_format_modal import NewFormatModal
from layout.modals.thumb_modal import ThumbModal
from layout.modals.upload_modal import UploadModal
from layout.windows.window import Window
from utils import update_image


class MainWindow(Window):
    def __init__(self):
        layout = [
            [
                sg.Menu(
                    [
                        [
                            "File",
                            [
                                "Import",
                                "Export",
                                ["Thumb", "Low quality", "New format"],
                            ],
                        ],
                        ["Filters", ["B&W", "Sepia", "Custom", "Colors"]],
                    ]
                )
            ],
            [sg.Image(key="-IMAGE-", expand_x=True, expand_y=True)],
        ]
        func_map = {
            "Import": self.load_image,
            "Thumb": self.save_thumb,
            "Low quality": self.save_low_quality,
            "New format": self.save_new_format,
            "BW": self.aply_bw_filter,
            "Sepia": self.aply_sepia_filter,
            "Custom": self.customWhite,
            "Colors": self.colorFilter,
        }
        super().__init__(layout, func_map)
        self.current_image = None
        self.path = None

    def start(self):
        super().start("Sputnick Photo Editor")

    def load_image(self, value: dict):
        modal = UploadModal()
        self.current_image, self.path = modal.start()
        update_image(self.current_image, self.window)

    def save_thumb(self, value: dict):
        modal = ThumbModal(self.current_image, self.path)
        modal.start()

    def save_low_quality(self, value: dict):
        modal = LowQualityModal(self.current_image, self.path)
        modal.start()

    def save_new_format(self, value: dict):
        modal = NewFormatModal(self.current_image, self.path)
        modal.start()

    def customWhite(self, value: dict):
        modal = CustomFilterModal(self.current_image)
        self.current_image = modal.start()
        update_image(self.current_image, self.window)

    def colorFilter(self, value: dict):
        modal = ColorFilterModal(self.current_image)
        self.current_image = modal.start()
        update_image(self.current_image, self.window)

    def applyFilter(self, filter):
        self.current_image = filter.apply(self.current_image)
        update_image(self.current_image, self.window)

    def aply_bw_filter(self, value: dict):
        self.applyFilter(BwFilter())

    def aply_sepia_filter(self, value: dict):
        self.applyFilter(SepiaFilter())
