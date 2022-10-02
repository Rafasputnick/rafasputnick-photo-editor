from PIL import Image

from layout.modals.modals_module import *


def invert_image(image: Image):
    return image.transpose(Image.FLIP_TOP_BOTTOM)

def resize_image(image: Image):
    modal = ResizeModal(image.size)
    size = modal.start()
    return image.resize(size)
    
def rotate_image(image: Image):
    modal = RotateModal()
    degrees_to_rotate = modal.start()
    return image.rotate(degrees_to_rotate)