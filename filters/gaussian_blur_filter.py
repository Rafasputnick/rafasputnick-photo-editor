from PIL import Image

from PIL import ImageFilter

from filters.filter import Filter

class GaussianBlurFilter(Filter):
    def apply(self, image: Image):
        image.filter(ImageFilter.GaussianBlur)