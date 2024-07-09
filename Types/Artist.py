class Artist:
    def __init__(self, name, artist_id, genres=None, images=None, popularity=None):
        self.name = name
        self.artist_id = artist_id
        self.genres = genres
        self.images = images
        self.popularity = popularity