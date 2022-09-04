import PySimpleGUI as sg

class Window:
    def __init__(self, layout: list, mapa_funcoes: dict):
        self.layout = layout
        self.mapa_funcoes = mapa_funcoes
        self.window = None


    def close_window(self):
        self.window.close()

    def handle_event(self, event: str, value: dict) -> str:
        if event in self.mapa_funcoes:
            return self.mapa_funcoes[event](value)
        else:
            print()

    def start(self, windows_name: str, is_modal: bool = False):
        self.window = sg.Window(windows_name, layout=self.layout, modal=is_modal)

        event = True
        keep_open = True
        while event != "Exit" and event != sg.WINDOW_CLOSED and keep_open:
            event, value = self.window.read()
            keep_open = self.handle_event(event, value)

        self.close_window()
        