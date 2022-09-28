import webbrowser

import PySimpleGUI as sg
from layout.windows.window import Window
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS


class InfoModal(Window):
    def __init__(self, image: Image, filename: str):
        if not image:
            raise Exception("Image not found")

        self.current_image = image

        fields = {
            "Model": "Camera Model",
            "ExifImageWidth": "Width",
            "ExifImageHeight": "Height",
            "DateTime": "Creating Date",
            "static_line": "*",
            "MaxApertureValue": "Aperture",
            "ExposureTime": "Exposure",
            "FNumber": "F-Stop",
            "Flash": "Flash",
            "FocalLength": "Focal Length",
            "ISOSpeedRatings": "ISO",
            "ShutterSpeedValue": "Shutter Speed",
        }

        self.info_map = self.get_info_map()
        long_filename = filename + image.format
        layout = [
            [
                sg.Text("File name", size=(10, 1)),
                sg.Text(long_filename, size=(25, 1)),
            ]
        ]
        for key, value in fields.items():
            info = self.info_map[key] if self.info_map.get(key) else "No data"
            layout += [
                [
                    sg.Text(value, size=(10, 1)),
                    sg.Text(info, size=(25, 1)),
                ]
            ]

        layout += [[sg.Button("Geolocalization"), sg.Button("Close")]]

        func_map_with_value = {}
        func_map = {"Close": self.close, "Geolocalization": self.open_google_maps}
        super().__init__(layout, func_map_with_value, func_map)

    def start(self):
        super().start("Image info", True)

    def get_info_map(self):
        exif_data = {}
        try:
            info = self.current_image._getexif()
        except OSError:
            info = {}

        # Se não encontrar o arquivo
        if info is None:
            info = {}
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for gps_tag in value:
                    sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                    gps_data[sub_decoded] = value[gps_tag]
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

        return exif_data

    def open_google_maps(self):

        gps_info = self.info_map["GPSInfo"]

        north = gps_info["GPSLatitude"]
        east = gps_info["GPSLongitude"]

        latitude = float(((north[0] * 60 + north[1]) * 60 + north[2]) / 3600)
        longitude = float(((east[0] * 60 + east[1]) * 60 + east[2]) / 3600)

        lat_ref = gps_info["GPSLatitudeRef"] if gps_info.get("GPSLatitudeRef") else "J"
        long_ref = (
            gps_info["GPSLongitudeRef"] if gps_info.get("GPSLongitudeRef") else "J"
        )

        if lat_ref != "N":
            latitude = 0 - latitude

        if long_ref != "E":
            longitude = 0 - longitude

        url = f"https://www.google.com.br/maps/search/{latitude},{longitude}/@{latitude},{longitude},17z"

        webbrowser.open(url)
