import PySimpleGUI as sg


class Window:
    def __init__(self, layout: list, func_map: dict, bind_map: dict = None):
        self.layout = layout
        self.func_map = func_map
        self.window = None
        self.keep_open = True
        self.bind_map = bind_map

    def close_window(self):
        self.window.close()

    def handle_event(self, event: str, value: dict) -> str:
        try:
            if event in self.func_map:
                return self.func_map[event](value)
            elif event != "Exit" and event != sg.WINDOW_CLOSED and self.keep_open:
                print("Erro ao encontrar evento")

        except Exception as error:
            sg.Popup("ERROR", error, icon="image/error.ico")

    def close(self):
        self.keep_open = False

    def start(self, windows_name: str, is_modal: bool = False):
        self.window = sg.Window(
            windows_name, layout=self.layout, modal=is_modal, icon="image/icon.ico"
        )

        if not is_modal:
            self.window.Resizable = True
            self.window.finalize().maximize()
            self.window.TKroot.minsize(1070, 600)

        self.define_binds()
        event = True
        while event != "Exit" and event != sg.WINDOW_CLOSED and self.keep_open:
            event, value = self.window.read()
            self.handle_event(event, value)

        self.close_window()

    def define_binds(self):
        if self.bind_map != None:
            for key, value in self.bind_map.items():
                self.window.bind(key, value)
