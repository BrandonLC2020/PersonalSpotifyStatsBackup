import json
import requests
import os
import time
import string
import random
import base64
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from Types.Album import Album
from Types.Artist import Artist
from Types.Image import Image
from Types.Track import Track
from Types.TrackFeatures import TrackFeatures

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
    
class SpotifyAPIManager():
    def __init__(self):     
        self.state = self.generate_random_state(16)
        self.auth_code = ''
        self.access_token = ''
        self.token_type = ''
        self.refresh_token = ''
        self.secrets_client = boto3.client("secretsmanager")
        self.secret_name = os.getenv('SECRET_NAME')
        self.refresh_token = self.get_secret()
        self.get_access_token_from_refresh_token()
        
    def generate_random_state(self, length):
        letters = string.ascii_letters
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string
        

    def get_access_token(self, code): 
        url = 'https://accounts.spotify.com/api/token'
        client_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
        client_string_bytes = client_string.encode("ascii") 
        
        base64_bytes = base64.b64encode(client_string_bytes) 
        base64_string = base64_bytes.decode("ascii") 
        headers = { 
            'Authorization' : 'Basic ' + base64_string,
            'Content-Type' : 'application/x-www-form-urlencoded' 
        }
        params = {
            'grant_type' : 'authorization_code',
            'redirect_uri' : REDIRECT_URI,
            'code' : code
        } 
        try:
            access_response = requests.post(url, params=params, headers=headers)

            if access_response.status_code == 200:
                access_json = access_response.json()
                self.access_token = access_json['access_token']
                self.token_type = access_json['token_type']
                self.refresh_token = access_json['refresh_token']
                print(self.refresh_token)
            else:
                print('Error:', access_response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None
        
    def get_secret(self):
        try:
            response = self.secrets_client.get_secret_value(SecretId=self.secret_name)
            secret = json.loads(response['SecretString'])
            return secret.get('spotify_refresh_token')
        except Exception as e:
            print(f"Error retrieving secret: {e}")
            return None
        
    def update_secret(self, new_token):
        try:
            self.secrets_client.update_secret(
                SecretId=self.secret_name,
                SecretString=json.dumps({'spotify_refresh_token': new_token})
            )
            print("Secret updated successfully.")
        except Exception as e:
            print(f"Error updating secret: {e}")
        
    def get_access_token_from_refresh_token(self): 
        url = 'https://accounts.spotify.com/api/token'
        client_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
        client_string_bytes = client_string.encode("ascii") 
        
        base64_bytes = base64.b64encode(client_string_bytes) 
        base64_string = base64_bytes.decode("ascii") 
        headers = { 
            'Authorization' : 'Basic ' + base64_string,
            'Content-Type' : 'application/x-www-form-urlencoded' 
        }
        params = {
            'grant_type' : 'refresh_token',
            'redirect_uri' : REDIRECT_URI,
            'refresh_token' : self.get_secret()
        } 
        try:
            access_response = requests.post(url, params=params, headers=headers)

            if access_response.status_code == 200:
                access_json = access_response.json()
                self.access_token = access_json['access_token']
                self.token_type = access_json['token_type']
                if 'refresh_token' in access_json:
                    self.refresh_token = access_json['refresh_token']
                    self.update_secret(self.refresh_token)
                print(self.refresh_token)
            else:
                print('Error:', access_response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None

    def get_top_tracks(self):
        url = 'https://api.spotify.com/v1/me/top/tracks'
        params = {
            'time_range' : 'short_term',
            'limit' : '50',
            'offset' : '0'
        } 
        headers = { 
            'Authorization' : f"{self.token_type} {self.access_token}",
            'Content-Type': 'application/json' 
        }
        try:
            top_tracks_response = requests.get(url, headers=headers, params=params)
            if top_tracks_response.status_code == 200:
                top_tracks_json = top_tracks_response.json()
                top_tracks_list = []
                for track in top_tracks_json['items']:
                    artists = []
                    for artist in track['artists']:
                        artists.append(Artist(name=artist['name'], artist_id=artist['id']))
                    album_images = []
                    for image in track['album']['images']:
                        album_images.append(Image(url=image['url'], height=image['height'], width=image['width']))
                    album_artists = []
                    for artist in track['album']['artists']:
                        album_artists.append(Artist(name=artist['name'], artist_id=artist['id']))
                    album = Album(name=track['album']['name'], album_id=track['album']['id'], 
                        album_type=track['album']['album_type'], release_date=track['album']['release_date'], 
                        images=album_images, artists=album_artists)
                    track_features = self.get_track_audio_features(track['id'])
                    top_tracks_list.append(Track(name=track['name'], track_id=track['id'], 
                        duration=track['duration_ms'], explicit=track['explicit'], disc_number=track['disc_number'], 
                        track_number=track['track_number'], artists=artists, album=album, popularity=track['popularity'], track_features=track_features))
                return top_tracks_list
            else:
                print('Error:', top_tracks_response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None

    def get_top_artists(self):
        url = 'https://api.spotify.com/v1/me/top/artists'
        headers = { 
            'Authorization' : f"{self.token_type} {self.access_token}",
            'Content-Type' : 'application/json' 
        }
        params = {
            'time_range' : 'short_term',
            'limit' : '50',
            'offset' : '0'
        } 
        try:
            top_artists_response = requests.get(url, headers=headers, params=params)
            if top_artists_response.status_code == 200:
                top_artists_json = top_artists_response.json()
                top_artists_list = []
                for artist in top_artists_json['items']:
                    artist_images = []
                    for image in artist['images']:
                        artist_images.append(Image(url=image['url'], height=image['height'], width=image['width']))
                    genres_list = []
                    for genre in artist['genres']:
                        genres_list.append(genre)
                    top_artists_list.append(Artist(name=artist['name'], artist_id=artist['id'], genres=genres_list, 
                        images=artist_images, popularity=artist['popularity']))
                return top_artists_list
            else:
                print('Error:', top_artists_response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None 
        
    def get_track_audio_features(self, track_id): # track_id is a single string
        url = f"https://api.spotify.com/v1/audio-features/{track_id}"
        headers = { 
            'Authorization' : f"{self.token_type} {self.access_token}",
            'Content-Type' : 'application/json'  
        }
        try:
            tracks_audio_features_response = requests.get(url, headers=headers)

            if tracks_audio_features_response.status_code == 200:
                tracks_audio_features_json = tracks_audio_features_response.json()
                return TrackFeatures(acousticness=tracks_audio_features_json['acousticness'], danceability=tracks_audio_features_json['danceability'], 
                    energy=tracks_audio_features_json['energy'], instrumentalness=tracks_audio_features_json['instrumentalness'], 
                    liveness=tracks_audio_features_json['liveness'], loudness=tracks_audio_features_json['loudness'], 
                    speechiness=tracks_audio_features_json['speechiness'], tempo=tracks_audio_features_json['tempo'], 
                    valence=tracks_audio_features_json['valence'])
            else:
                print('Error:', tracks_audio_features_response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None  