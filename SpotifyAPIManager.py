import requests
import os
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def get_access_token(): 
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

def main():
    get_access_token()

if __name__ == '__main__':
    main()