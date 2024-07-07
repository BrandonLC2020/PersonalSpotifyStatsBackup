class Track:
    def __init__(self, name, track_id, duration, explicit, disc_number, track_number, popularity, artists, album):
        self.name = name
        self.track_id = track_id
        self.duration = duration # in milliseconds
        self.is_explicit = explicit
        self.disc_number = disc_number
        self.track_number = track_number
        self.popularity = popularity
        self.album = album
        self.artists = artists