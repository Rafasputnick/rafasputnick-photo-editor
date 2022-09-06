import PySimpleGUI as sg
from filters.bw_filter import BwFilter
from filters.sepia_filter import SepiaFilter
from layout.modals.color_filter_modal import ColorFilterModal
from layout.modals.custom_filter_modal import CustomFilterModal
from layout.modals.export_modal import ExportModal
from layout.modals.import_modal import ImportModal
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
                                "Export"
                            ],
                        ],
                        ["Filters", ["B&W", "Sepia", "Custom", "Colors"]],
                    ]
                )
            ],
            [sg.Image(key="-IMAGE-", expand_x=True, expand_y=True)],
        ]
        func_map = {
            "Import": self.import_image,
            "Export": self.export_image,
            "BW": self.aply_bw_filter,
            "Sepia": self.aply_sepia_filter,
            "Custom": self.customWhite,
            "Colors": self.colorFilter,
        }
        super().__init__(layout, func_map)
        self.current_image = None

    def start(self):
        super().start("Sputnick Photo Editor")

    def import_image(self, value: dict):
        modal = ImportModal()
        self.current_image = modal.start()
        update_image(self.current_image, self.window)

    def export_image(self, value: dict):
        modal = ExportModal(self.current_image, "")
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
