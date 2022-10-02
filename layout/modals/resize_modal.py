import PySimpleGUI as sg
from layout.windows.window import Window


class ResizeModal(Window):
    def __init__(self, current_size: tuple):
        layout = [
            [
                sg.Text("Choose the new size:"),
            ],
            [
                sg.Text("Width:"),
                sg.Input(size=(25, 1), key="-WIDTH-", default_text=current_size[0]),
            ],
            [
                sg.Text("Height:"),
                sg.Input(size=(25, 1), key="-HEIGHT-", default_text=current_size[1]),
            ],
            [
                sg.Button("Apply"),
            ],
        ]
        func_map_with_values = {"Apply": self.aply_change}
        func_map = {}
        super().__init__(layout, func_map_with_values, func_map)
        self.new_size = None

    def start(self):
        super().start("Set new size", True)
        return self.new_size

    def aply_change(self, value: dict):
        height = int(value["-HEIGHT-"])
        width = int(value["-WIDTH-"])
        self.new_size = tuple((width, height))
        self.close()
