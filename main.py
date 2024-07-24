from Managers.DatabaseManager import DatabaseManager
from Types.MonthlyTopAlbums import MonthlyTopAlbums
from Types.MonthlyTopArtists import MonthlyTopArtists
from Types.MonthlyTopTracks import MonthlyTopTracks
from Managers.SpotifyAPIManager import SpotifyAPIManager

spotify_api_manager = SpotifyAPIManager()
database_manager = DatabaseManager()
top_tracks_obj = spotify_api_manager.get_top_tracks()
last_month_top_tracks = MonthlyTopTracks(top_tracks_obj)
last_month_top_artists = MonthlyTopArtists(spotify_api_manager.get_top_artists())
last_month_top_albums = MonthlyTopAlbums(top_tracks_obj)
database_manager.insert_top_artists_into_db(last_month_top_artists)
database_manager.insert_top_tracks_into_db(last_month_top_tracks)
database_manager.insert_top_albums_into_db(last_month_top_albums)