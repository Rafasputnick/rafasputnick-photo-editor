from PIL import Image

from utils import set_palette

from filters.filter import Filter

class SepiaFilter(Filter):
    def apply(self, image: Image):
        white = (255,240,192)
        palette = set_palette(white)

        image = image.convert("L")
        image.putpalette(palette)
        return image