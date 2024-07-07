import requests
import os
import time
import string
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import base64
from dotenv import load_dotenv


load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI_LOCAL')
SPOTIFY_USERNAME = os.getenv('SPOTIFY_USERNAME')
SPOTIFY_PASSWORD = os.getenv('SPOTIFY_PASSWORD')

def generate_random_string(length):
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def get_user_authorization(state):
    url = 'https://accounts.spotify.com/authorize'
    params = {
        'state' : state,
        'scope' : 'user-read-private user-read-email user-top-read',
        'response_type' : 'code',
        'redirect_uri' : REDIRECT_URI,
        'client_id' : CLIENT_ID
    }
    try:
        authorization_response = requests.get(url, params=params)
        print(authorization_response.url)
        driver = webdriver.Firefox()

        driver.get(authorization_response.url)
        if driver.title == 'Login - Spotify':
            username_text_field = driver.find_element(By.ID, 'login-username')
            username_text_field.send_keys(SPOTIFY_USERNAME)
            password_text_field = driver.find_element(By.ID, 'login-password')
            password_text_field.send_keys(SPOTIFY_PASSWORD)
            enter_credentials_link = driver.find_element(By.ID, 'login-button')
            enter_credentials_link.click()
            timeDelay = 0
            while (driver.title == 'Login - Spotify'):
                timeDelay += 1
            while driver.title == 'Spotify':
                timeDelay += 1
            driver.implicitly_wait(2)
            visit_site_button = driver.find_element(By.CSS_SELECTOR, 'button.ring-blue-600\/20')
            visit_site_button.click()
        driver.quit()

    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
    
class SpotifyAPIManager():
    def __init__(self):     
        self.state = generate_random_string(16)
        self.auth_code = ''
        self.access_token = ''
        self.token_type = ''
        get_user_authorization(self.state)
        file_path = 'authorization.txt'

        while not os.path.exists(file_path):
            time.sleep(1)

        if os.path.isfile(file_path):
            authorization_file = open(file_path, 'r')
            authorization_info = authorization_file.readline()
            authorization_info_list = authorization_info.split(' ')
            self.auth_code = authorization_info_list[0]
            state_returned = authorization_info_list[1]
            if state_returned != self.state:
                return
            else:
                os.remove(file_path)
            self.get_access_token(self.auth_code)
        else:
            raise ValueError("%s isn't a file!" % file_path)

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
                return top_tracks_json
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
                return top_artists_json
            else:
                print('Error:', top_artists_response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None 
    
    def get_tracks_audio_features(self, track_ids): #track_ids is a list of strings
        track_ids_str = ','.join(track_ids)
        url = f"https://api.spotify.com/v1/audio-features"
        params = { 'ids': track_ids_str }
        headers = { 
            'Authorization' : f"{self.token_type} {self.access_token}",
            'Content-Type' : 'application/json'  
        }
        try:
            tracks_audio_features_response = requests.get(url, headers=headers, params=params)

            if tracks_audio_features_response.status_code == 200:
                tracks_audio_features_json = tracks_audio_features_response.json()
                return tracks_audio_features_json
            else:
                print('Error:', tracks_audio_features_response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None
        
    def get_tracks_audio_analysis(self, track_id):
        url = f"https://api.spotify.com/v1/audio-analysis/{track_id}"
        headers = { 
            'Authorization' : f"{self.token_type} {self.access_token}",
            'Content-Type' : 'application/json'  
        }
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