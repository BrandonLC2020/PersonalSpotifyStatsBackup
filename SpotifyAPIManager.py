import requests
import os
import string
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv


load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI_LOCAL')

def generate_random_string(length):
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def get_user_authorization():
    url = 'https://accounts.spotify.com/authorize'
    params = {
        'state' : generate_random_string(16),
        'scope' : 'user-read-private user-read-email user-top-read',
        'response_type' : 'code',
        'redirect_uri' : REDIRECT_URI,
        'client_id' : CLIENT_ID
    }
    try:
        authorization_response = requests.get(url, params=params)
        print(authorization_response.url)
        driver = webdriver.Firefox()

        # Navigate to a webpage
        driver.get(authorization_response.url)

        usernameText = driver.find_element(By.NAME, 'Email or username')

        # Close the browser
        #driver.quit()

    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None


class SpotifyAPIManager:
    def __init__(self):        
        self.authorization_info = get_user_authorization()

    def get_access_token(self): 
        url = 'https://accounts.spotify.com/api/token'
        headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
        data = f"grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"
        try:
            access_response = requests.post(url, data=data, headers=headers)

            if access_response.status_code == 200:
                access_json = access_response.json()
                access_token = access_json['access_token']
                access_token_type = access_json['token_type']
                return access_token, access_token_type
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
        headers = { 'Authorization' : f"{self.token_type} {self.access_token}",
                   "Content-Type": "application/json" }
        try:
            top_tracks_response = requests.get(url, headers=headers, params=params)

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
        headers = { 'Authorization' : f"{self.token_type} {self.access_token}" }
        try:
            top_artists_response = requests.get(url, headers=headers)

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
        headers = { 'Authorization' : f"{self.token_type} {self.access_token}" }
        try:
            tracks_audio_features_response = requests.get(url, headers=headers)

            if tracks_audio_features_response.status_code == 200:
                tracks_audio_features_json = tracks_audio_features_response.json()
                return tracks_audio_features_json
            else:
                print('Error:', tracks_audio_features_response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None 