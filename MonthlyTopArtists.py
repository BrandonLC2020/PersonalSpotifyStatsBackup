from datetime import date, timedelta

class MonthlyTopArtists:
    def __init__(self, top_artists):
        top_artists_dict = {}
        for track in top_artists:
            top_artists_dict[top_artists.index(track) + 1] = track
        self.top_artists = top_artists_dict
        prev = date.today().replace(day=1) - timedelta(days=1)
        self.month = prev.month
        self.year = prev.year
        