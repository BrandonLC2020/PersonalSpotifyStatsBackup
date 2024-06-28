import requests

def get_access_token(): 
    url = 'https://accounts.spotify.com/api/token'
    headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
    data = 'grant_type=client_credentials&client_id=your-client-id&client_secret=your-client-secret'