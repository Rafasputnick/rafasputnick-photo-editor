from PIL import Image

from PIL import ImageFilter

from filters.filter import Filter

class DetailFilter(Filter):
    def apply(self, image: Image):
        return image.filter(ImageFilter.DETAIL)