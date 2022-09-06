from PIL import Image

from utils import set_palette

from filters.filter import Filter

class CustomWhiteFilter(Filter):

    def __init__(self, new_white: tuple):
        self.new_white = new_white
        super().__init__()

    def apply(self, image: Image):
        palette = set_palette(self.new_white)

        image = image.convert("L")
        image.putpalette(palette)
        return image