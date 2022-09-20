from PIL import Image

from PIL import ImageFilter

from filters.filter import Filter


class BlurFilter(Filter):
    def apply(self, image: Image):
        return image.filter(ImageFilter.BLUR)
