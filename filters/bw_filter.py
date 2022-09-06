from PIL import Image

from filters.filter import Filter

class BwFilter(Filter):
    def apply(self, image: Image):
        return image.convert('L')