from PIL import Image

from PIL import ImageFilter

from filters.filter import Filter

class SharpenFilter(Filter):
    def apply(self, image: Image):
        image.filter(ImageFilter.SHARPEN)