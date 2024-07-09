from DatabaseManager import DatabaseManager
from Types.MonthlyTopArtists import MonthlyTopArtists
from Types.MonthlyTopTracks import MonthlyTopTracks
from SpotifyAPIManager import SpotifyAPIManager

spotify_api_manager = SpotifyAPIManager()
# database_manager = DatabaseManager()
last_month_top_tracks = MonthlyTopTracks(spotify_api_manager.get_top_tracks())
last_month_top_artists = MonthlyTopArtists(spotify_api_manager.get_top_artists())