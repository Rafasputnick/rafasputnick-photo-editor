from PIL import Image

from filters.filter import Filter


class ColorFilter(Filter):
    def apply(self, image: Image, num_color: int):
        return image.convert("P", palette=Image.Palette.ADAPTIVE, colors=num_color)
