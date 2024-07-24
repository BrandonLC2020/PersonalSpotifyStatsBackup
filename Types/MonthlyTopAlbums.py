from datetime import date, timedelta
import numpy as np

from Types.Album import Album
from Types.Track import Track

class MonthlyTopAlbums:
    def __init__(self, top_tracks : list[Track]):
        top_tracks_dict = {}
        for track in top_tracks:
            top_tracks_dict[top_tracks.index(track) + 1] = track
        self.top_tracks : dict[int, Track] = top_tracks_dict
        prev = date.today().replace(day=1) - timedelta(days=1)
        self.month = prev.month
        self.year = prev.year
        all_albums_list : list[Album ]= []
        for track in top_tracks:
            all_albums_list.append(track.album)
        album_ids_and_counts : dict[str, int] = {}
        for album in all_albums_list:
            if album.album_id not in album_ids_and_counts.keys():
                album_ids_and_counts[album.album_id] = 1
            else:
                album_ids_and_counts[album.album_id] = album_ids_and_counts[album.album_id] + 1
        counts_and_albums : dict[int, list[Album]] = {}
        for album_id, count in album_ids_and_counts.items():
            if count > 1:
                album_to_add = next((x for x in all_albums_list if x.album_id == album_id), None)
                if album_to_add != None:
                    if count not in counts_and_albums.keys():
                        counts_and_albums[count] = [album_to_add]
                    else:
                        counts_and_albums[count] = counts_and_albums[count].append(album_to_add)
        ranks_and_sorted_albums : dict[int, list[Album]] = {}
        for rank in sorted(counts_and_albums.keys(), reverse=True):
            ranks_and_sorted_albums[rank] = sorted(counts_and_albums.values(), key=lambda album: album.name)
        self.top_albums : dict[int, list[Album]] = ranks_and_sorted_albums.copy()

