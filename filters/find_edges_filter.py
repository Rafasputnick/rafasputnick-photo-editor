from PIL import Image

from PIL import ImageFilter

from filters.filter import Filter

class FindEdgesFilter(Filter):
    def apply(self, image: Image):
        return image.filter(ImageFilter.FIND_EDGES)