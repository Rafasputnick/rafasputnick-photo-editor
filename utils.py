import io
import os

from PIL import Image
from PySimpleGUI import Window


def update_image(image: Image, window: Window):
    if image:
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        window["-IMAGE-"].update(data=bio.getvalue(), size=(500, 500))


def set_palette(white: tuple):
    palette = []
    r, g, b = white
    for i in range(255):
        new_red = r * i // 255
        new_green = g * i // 255
        new_blue = b * i // 255
        palette.extend((new_red, new_green, new_blue))
    return palette
