from PIL import Image, ImageEnhance

from layout.modals.modals_module import *


def enhance_brightness(image: Image):
    return enhance_process(ImageEnhance.Brightness(image), EnhanceModal("Brightness"))


def enhance_contrast(image: Image):
    return enhance_process(ImageEnhance.Contrast(image), EnhanceModal("Contrast"))


def enhance_color(image: Image):
    return enhance_process(ImageEnhance.Color(image), EnhanceModal("Color"))


def enhance_sharpness(image: Image):
    return enhance_process(ImageEnhance.Sharpness(image), EnhanceModal("Sharpness"))


def enhance_process(enhancer, modal):
    enhance_factor = modal.start()
    return enhancer.enhance(enhance_factor)
    