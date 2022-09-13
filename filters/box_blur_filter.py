from PIL import Image

from PIL import ImageFilter

from filters.filter import Filter

class BoxBlurFilter(Filter):
    def apply(self, image: Image):
        image.filter(ImageFilter.BoxBlur(radius=3))