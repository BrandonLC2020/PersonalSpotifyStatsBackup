from Types.Image import Image


class Artist:
    def __init__(self, name, artist_id, genres=None, images=None, popularity=None):
        self.name = name
        self.artist_id = artist_id
        self.genres : list[str] = genres
        self.images : list[Image] = images
        self.popularity = popularity