class Album:
    def __init__(self, name, album_id, album_type, images, artists, release_date):
        self.album_type = album_type
        self.album_id = album_id
        self.images = images
        self.name = name
        self.artists = artists
        self.release_date = release_date
