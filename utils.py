import io
from PySimpleGUI import Window

from layout.windows.state_image import StateImage


def update_image(
    state_image: StateImage, window: Window, shortcut, register_change: bool = True
):
    if state_image:
        bio = io.BytesIO()
        image = state_image.current_image
        image.save(bio, format="PNG")
        img_object = window["-IMAGE-"].draw_image(data=bio.getvalue(), location=(0, 500))
        if register_change:
            shortcut.register_change(state_image)
        return img_object


def set_palette(white: tuple):
    palette = []
    r, g, b = white
    for i in range(255):
        new_red = r * i // 255
        new_green = g * i // 255
        new_blue = b * i // 255
        palette.extend((new_red, new_green, new_blue))
    return palette
