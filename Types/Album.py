from Types.Artist import Artist
from Types.Image import Image


class Album:
    def __init__(self, name, album_id, album_type, images, artists, release_date):
        self.album_type = album_type
        self.album_id = album_id
        self.images : list[Image] = images
        self.name = name
        self.artists : list[Artist] = artists
        self.release_date = release_date