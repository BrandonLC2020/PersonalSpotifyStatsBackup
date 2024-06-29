import requests
import os
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def get_access_token(self): 
        url = 'https://accounts.spotify.com/api/token'
        headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
        data = f"grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"
        try:
            access_token_response = requests.post(url, data=data, headers=headers)

            if access_token_response.status_code == 200:
                access_token_json = access_token_response.json()
                access_token = access_token_json['access_token']
                return access_token
            else:
                print('Error:', access_token_response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None


class SpotifyAPIManager:
    def __init__(self):
        self.access_token = get_access_token()

    def get_top_tracks(self):
        url = 'https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=50&offset=0'
        headers = { 'Authorization' : f"Bearer {self.access_token}" }
        try:
            top_tracks_response = requests.post(url, headers=headers)

            if top_tracks_response.status_code == 200:
                top_tracks_json = top_tracks_response.json()
                return top_tracks_json
            else:
                print('Error:', top_tracks_response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None

    def get_top_artists(self):
        url = 'https://api.spotify.com/v1/me/top/artists?time_range=short_term&limit=50&offset=0'
        headers = { 'Authorization' : f"Bearer {self.access_token}" }
        try:
            top_artists_response = requests.post(url, headers=headers)

            if top_artists_response.status_code == 200:
                top_artists_json = top_artists_response.json()
                return top_artists_json
            else:
                print('Error:', top_artists_response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None 
    
    def get_tracks_audio_features(self, track_ids): #track_ids is a list of strings
        track_ids_str = ','.join(track_ids)
        url = f"https://api.spotify.com/v1/audio-features?ids={track_ids_str}"
        headers = { 'Authorization' : f"Bearer {self.access_token}" }
        try:
            tracks_audio_features_response = requests.post(url, headers=headers)

            if tracks_audio_features_response.status_code == 200:
                tracks_audio_features_json = tracks_audio_features_response.json()
                return tracks_audio_features_json
            else:
                print('Error:', tracks_audio_features_response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None 