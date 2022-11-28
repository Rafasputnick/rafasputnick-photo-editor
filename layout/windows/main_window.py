import copy

import PySimpleGUI as sg
from enhances import *
from filters import *
from layout.modals.modals_module import *
from layout.shortcut.shortcuts_module import *
from layout.windows.state_image import StateImage
from layout.windows.window import Window
from transformations import *
from utils import update_image


class MainWindow(Window):
    def __init__(self):
        self.shortcut = UndoReundo()
        self.image_state = StateImage()
        self.dragging = False
        self.rectangle = None
        self.rectangle_initial = None
        self.end_rectangle = None
        self.img_object = None
        self.selection_visible = False
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
                        ["Trasform", ["Crop Selection", "Invert", "Resize", "Rotate"]],
                        ["Enhance", ["Brightness", "Contrast", "Color", "Sharpness"]],
                    ]
                )
            ],
            [
                sg.Graph(
                    key="-IMAGE-",
                    canvas_size=(500, 500),
                    expand_x = True,
                    expand_y = True,
                    graph_bottom_left=(0, 0),
                    graph_top_right=(500, 500),
                    change_submits=True,
                    drag_submits=True,
                )
            ],
        ]
        func_map_with_value = {"-IMAGE-": self.draw_crop_area}
        func_map = {
            "Import": self.import_image,
            "Export as": self.export_image,
            "Save": self.save,
            "Info": self.show_info,
            "Undo": self.undo,
            "Reundo": self.reundo,
            "Custom": [self.apply_change, custom_white_filter],
            "Colors": [self.apply_change, color_filter],
            "BW": [self.apply_change, bw_filter],
            "Sepia": [self.apply_change, sepia_filter],
            "Blur": [self.apply_change, blur_filter],
            "Box Blur": [self.apply_change, box_blur_filter],
            "Countour": [self.apply_change, countour_filter],
            "Detail": [self.apply_change, datail_filter],
            "Smooth": [self.apply_change, smooth_filter],
            "Sharpen": [self.apply_change, sharpen_filter],
            "Gaussian Blur": [self.apply_change, gaussian_blur_filter],
            "Finding edges": [self.apply_change, finding_edges_filter],
            "Emboss": [self.apply_change, emboss_filter],
            "Edge Enhance": [self.apply_change, edge_enhance_filter],
            "Invert": [self.apply_change, invert_image],
            "Resize": [self.apply_change, resize_image],
            "Rotate": [self.apply_change, rotate_image],
            "Brightness": [self.apply_change, enhance_brightness],
            "Contrast": [self.apply_change, enhance_contrast],
            "Color": [self.apply_change, enhance_color],
            "Sharpness": [self.apply_change, enhance_sharpness],
            "-IMAGE-+UP": self.crop_area_selected,
            "Crop Selection": self.set_selection_visible,
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

    def set_selection_visible(self):
        if self.image_state.current_image != None:
            self.selection_visible = True

    def crop_area_selected(self):
        if self.selection_visible:

            self.dragging = False
            x1 = min(self.rectangle_initial[0], self.end_rectangle[0])
            y1 = 500 - max(self.rectangle_initial[1], self.end_rectangle[1])

            x2 = max(self.rectangle_initial[0], self.end_rectangle[0])
            y2 = 500 - min(self.rectangle_initial[1], self.end_rectangle[1])

            new_state = self.clone_image_state()
            new_state.current_image = new_state.current_image.crop((x1, y1, x2, y2))
            self.window["-IMAGE-"].delete_figure(self.rectangle)
            self.img_object = update_image(new_state, self.window, self.shortcut)
            self.image_state = new_state
            self.selection_visible = False

    def draw_crop_area(self, value: dict):
        if self.selection_visible:
            x, y = value["-IMAGE-"]
            if not self.dragging:
                self.rectangle_initial = (x, y)
                self.dragging = True
            else:
                self.end_rectangle = (x, y)
            if self.rectangle:
                self.window["-IMAGE-"].delete_figure(self.rectangle)
            if None not in (self.rectangle_initial, self.end_rectangle):
                self.rectangle = self.window["-IMAGE-"].draw_rectangle(
                    self.rectangle_initial, self.end_rectangle, line_color="red"
                )

    def clone_image_state(self):
        if self.image_state.current_image != None:
            self.window["-IMAGE-"].delete_figure(self.img_object)
        return copy.deepcopy(self.image_state)

    def import_image(self):
        new_state = self.clone_image_state()
        modal = ImportModal()
        new_state.current_image, new_state.filename = modal.start()
        self.img_object = update_image(new_state, self.window, self.shortcut)
        self.image_state = new_state

    def export_image(self):
        new_state = self.clone_image_state()
        modal = ExportModal(new_state.current_image, new_state.filename)
        new_state.current_image, new_state.filename = modal.start()
        self.img_object = update_image(new_state, self.window, self.shortcut)
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

    def apply_change(self, change_function):
        new_state = self.clone_image_state()
        new_state.current_image = change_function(new_state.current_image)
        self.img_object = update_image(new_state, self.window, self.shortcut)
        self.image_state = new_state

    def undo(self):
        new_state = self.clone_image_state()
        new_state, change = self.shortcut.undo()
        if change:
            self.img_object = update_image(new_state, self.window, self.shortcut, False)
            self.image_state = new_state

    def reundo(self):
        new_state = self.clone_image_state()
        new_state, change = self.shortcut.reundo()
        if change:
            self.img_object = update_image(new_state, self.window, self.shortcut, False)
            self.image_state = new_state
