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

    access_token_request = requests.post(url, data=data, headers=headers)
    print(access_token_request.text)

def main():
    get_access_token()

if __name__ == '__main__':
    main()