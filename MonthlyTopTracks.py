from datetime import date, timedelta

class MonthlyTopTracks:
    def __init__(self, top_tracks):
        top_tracks_dict = {}
        for track in top_tracks:
            top_tracks_dict[top_tracks.index(track) + 1] = track
        self.top_tracks = top_tracks_dict
        prev = date.today().replace(day=1) - timedelta(days=1)
        self.month = prev.month
        self.year = prev.year
        