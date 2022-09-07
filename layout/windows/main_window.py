import copy

import PySimpleGUI as sg
from filters.bw_filter import BwFilter
from filters.sepia_filter import SepiaFilter
from layout.modals.color_filter_modal import ColorFilterModal
from layout.modals.custom_filter_modal import CustomFilterModal
from layout.modals.export_modal import ExportModal
from layout.modals.import_modal import ImportModal
from layout.modals.info_modal import InfoModal
from layout.shortcut.undo_reundo import UndoReundo
from layout.windows.state_image import StateImage
from layout.windows.window import Window
from utils import update_image


class MainWindow(Window):
    def __init__(self):
        self.shortcut = UndoReundo()
        layout = [
            [
                sg.Menu(
                    [
                        [
                            "File",
                            ["Import", "Export as", "Save", "Info"],
                        ],
                        ["Filters", ["B&W", "Sepia", "Custom", "Colors"]],
                    ]
                )
            ],
            [sg.Image(key="-IMAGE-", expand_x=True, expand_y=True)],
        ]
        func_map = {
            "Import": self.import_image,
            "Export as": self.export_image,
            "Save": self.save,
            "Info": self.show_info,
            "BW": self.aply_bw_filter,
            "Sepia": self.aply_sepia_filter,
            "Custom": self.customWhite,
            "Colors": self.colorFilter,
            "Undo": self.undo,
            "Reundo": self.reundo,
        }
        bind_map = {
            "<Control-Shift-Key-Z>": "Reundo",
            "<Control-Shift-Key-z>": "Reundo",
            "<Control-Key-Z>": "Undo",
            "<Control-Key-z>": "Undo",
            "<Control-Key-S>": "Save",
            "<Control-Key-s>": "Save",
            "<Control-Shift-Key-S>": "Export as",
            "<Control-Shift-Key-s>": "Export as",
            "<Control-Key-O>": "Import",
            "<Control-Key-o>": "Import",
        }
        super().__init__(layout, func_map, bind_map)
        self.image_state = StateImage()

    def start(self):
        super().start("Sputnick Photo Editor")

    def clone_image_state(self):
        return copy.deepcopy(self.image_state)

    def import_image(self, value: dict):
        new_state = self.clone_image_state()
        modal = ImportModal()
        new_state.current_image, new_state.filename = modal.start()
        update_image(new_state, self.window, self.shortcut)
        self.image_state = new_state

    def export_image(self, value: dict):
        new_state = self.clone_image_state()
        modal = ExportModal(new_state.current_image, new_state.filename)
        new_state.current_image, new_state.filename = modal.start()
        update_image(new_state, self.window, self.shortcut)
        self.image_state = new_state

    def save(self, value: dict):
        format = (
            self.image_state.current_image.format
            if self.image_state.current_image.format
            else "png"
        )
        if self.image_state.current_image != None:
            path = "exports/" + self.image_state.filename + "." + str(format).lower()
            self.image_state.current_image.save(path)

    def show_info(self, value: dict):
        modal = InfoModal(self.image_state.current_image, self.image_state.filename)
        modal.start()

    def customWhite(self, value: dict):
        new_state = self.clone_image_state()
        modal = CustomFilterModal(new_state.current_image)
        new_state.current_image = modal.start()
        update_image(new_state, self.window, self.shortcut)
        self.image_state = new_state

    def colorFilter(self, value: dict):
        new_state = self.clone_image_state()
        modal = ColorFilterModal(new_state.current_image)
        new_state.current_image = modal.start()
        update_image(new_state, self.window, self.shortcut)
        self.image_state = new_state

    def applyFilter(self, filter):
        new_state = self.clone_image_state()
        new_state.current_image = filter.apply(new_state.current_image)
        update_image(new_state, self.window, self.shortcut)
        self.image_state = new_state

    def aply_bw_filter(self, value: dict):
        self.applyFilter(BwFilter())

    def aply_sepia_filter(self, value: dict):
        self.applyFilter(SepiaFilter())

    def undo(self, value: dict):
        new_state = self.clone_image_state()
        new_state, change = self.shortcut.undo()
        if change:
            update_image(new_state, self.window, self.shortcut, False)
            self.image_state = new_state

    def reundo(self, value: dict):
        new_state = self.clone_image_state()
        new_state, change = self.shortcut.reundo()
        if change:
            update_image(new_state, self.window, self.shortcut, False)
            self.image_state = new_state
