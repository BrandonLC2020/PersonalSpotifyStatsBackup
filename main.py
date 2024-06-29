from SpotifyAPIManager import SpotifyAPIManager

def main():
    spotify_api_manager = SpotifyAPIManager()
    print(spotify_api_manager.authorization_info)

if __name__ == '__main__':
    main()