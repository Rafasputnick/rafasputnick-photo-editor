from PIL import Image

from PIL import ImageFilter

from filters.filter import Filter

class EmbossFilter(Filter):
    def apply(self, image: Image):
        return image.filter(ImageFilter.EMBOSS)