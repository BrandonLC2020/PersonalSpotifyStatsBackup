from SpotifyAPIManager import SpotifyAPIManager

def main():
    spotify_api_manager = SpotifyAPIManager()
    print(spotify_api_manager.access_token)
    print(spotify_api_manager.token_type)
    print(spotify_api_manager.get_top_tracks())

if __name__ == '__main__':
    main()