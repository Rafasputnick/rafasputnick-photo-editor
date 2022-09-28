import copy

import PySimpleGUI as sg
from filters import *
from layout.modals.modals_module import *
from layout.shortcut.shortcuts_module import *
from layout.windows.state_image import StateImage
from layout.windows.window import Window
from utils import update_image


class MainWindow(Window):
    def __init__(self):
        self.shortcut = UndoReundo()
        self.image_state = StateImage()
        layout = [
            [
                sg.Menu(
                    [
                        [
                            "File",
                            ["Import", "Export as", "Save", "Info"],
                        ],
                        [
                            "Filters",
                            [
                                "B&W",
                                "Sepia",
                                "Custom",
                                "Colors",
                                "Blur",
                                "Box Blur",
                                "Countour",
                                "Gaussian Blur",
                                "Detail",
                                "Sharpen",
                                "Finding edges",
                                "Emboss",
                                "Edge Enhance",
                                "Smooth",
                            ],
                        ],
                    ]
                )
            ],
            [sg.Image(key="-IMAGE-", expand_x=True, expand_y=True)],
        ]
        func_map_with_value = { }
        func_map = {
            "Import": self.import_image,
            "Export as": self.export_image,
            "Save": self.save,
            "Info": self.show_info,
            "Undo": self.undo,
            "Reundo": self.reundo,
            "Custom": [self.applyFilter, custom_white_filter],
            "Colors": [self.applyFilter, color_filter],
            "BW": [self.applyFilter, bw_filter],
            "Sepia": [self.applyFilter, sepia_filter],
            "Blur": [self.applyFilter, blur_filter],
            "Box Blur": [self.applyFilter, box_blur_filter],
            "Countour": [self.applyFilter, countour_filter],
            "Detail": [self.applyFilter, datail_filter],
            "Smooth": [self.applyFilter, smooth_filter],
            "Sharpen": [self.applyFilter, sharpen_filter],
            "Gaussian Blur": [self.applyFilter, gaussian_blur_filter],
            "Finding edges": [self.applyFilter, finding_edges_filter],
            "Emboss": [self.applyFilter, emboss_filter],
            "Edge Enhance": [self.applyFilter, edge_enhance_filter],
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
        super().__init__(layout, func_map_with_value, func_map, bind_map)

    def start(self):
        super().start("Sputnick Photo Editor")

    def clone_image_state(self):
        return copy.deepcopy(self.image_state)

    def import_image(self):
        new_state = self.clone_image_state()
        modal = ImportModal()
        new_state.current_image, new_state.filename = modal.start()
        update_image(new_state, self.window, self.shortcut)
        self.image_state = new_state

    def export_image(self):
        new_state = self.clone_image_state()
        modal = ExportModal(new_state.current_image, new_state.filename)
        new_state.current_image, new_state.filename = modal.start()
        update_image(new_state, self.window, self.shortcut)
        self.image_state = new_state

    def save(self):
        format = (
            self.image_state.current_image.format
            if self.image_state.current_image.format
            else "png"
        )
        if self.image_state.current_image != None:
            path = "exports/" + self.image_state.filename + "." + str(format).lower()
            self.image_state.current_image.save(path)

    def show_info(self):
        modal = InfoModal(self.image_state.current_image, self.image_state.filename)
        modal.start()

    def applyFilter(self, filter):
        new_state = self.clone_image_state()
        new_state.current_image = filter(new_state.current_image)
        update_image(new_state, self.window, self.shortcut)
        self.image_state = new_state

    def undo(self):
        new_state = self.clone_image_state()
        new_state, change = self.shortcut.undo()
        if change:
            update_image(new_state, self.window, self.shortcut, False)
            self.image_state = new_state

    def reundo(self):
        new_state = self.clone_image_state()
        new_state, change = self.shortcut.reundo()
        if change:
            update_image(new_state, self.window, self.shortcut, False)
            self.image_state = new_state
