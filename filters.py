from PIL import Image, ImageFilter

from layout.modals.modals_module import *
from utils import *


def bw_filter(image: Image):
    return image.convert("L")


def sepia_filter(image: Image):
    white = (255, 240, 192)
    palette = set_palette(white)

    image = image.convert("L")
    image.putpalette(palette)
    return image


def blur_filter(image: Image):
    return image.filter(ImageFilter.BLUR)


def box_blur_filter(image: Image):
    return image.filter(ImageFilter.BoxBlur(radius=3))


def countour_filter(image: Image):
    return image.filter(ImageFilter.CONTOUR)


def datail_filter(image: Image):
    return image.filter(ImageFilter.DETAIL)


def edge_enhance_filter(image: Image):
    return image.filter(ImageFilter.EDGE_ENHANCE)


def emboss_filter(image: Image):
    return image.filter(ImageFilter.EMBOSS)


def finding_edges_filter(image: Image):
    return image.filter(ImageFilter.FIND_EDGES)


def gaussian_blur_filter(image: Image):
    return image.filter(ImageFilter.GaussianBlur)


def sharpen_filter(image: Image):
    return image.filter(ImageFilter.SHARPEN)


def smooth_filter(image: Image):
    return image.filter(ImageFilter.SMOOTH)


def color_filter(image: Image):
    modal = ColorFilterModal()
    num_color = modal.start()
    return image.convert("P", palette=Image.Palette.ADAPTIVE, colors=num_color)


def custom_white_filter(image: Image):
    modal = CustomFilterModal()
    new_white = modal.start()
    palette = set_palette(new_white)
    image = image.convert("L")
    image.putpalette(palette)
    return image
