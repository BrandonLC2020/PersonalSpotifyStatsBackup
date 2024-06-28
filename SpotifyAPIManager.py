import requests

def get_access_token(): 
    url = 'https://accounts.spotify.com/api/token'
    headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
    data = 'grant_type=client_credentials&client_id=your-client-id&client_secret=your-client-secret'

    access_token_request = requests.post(url, data=data, headers=headers)
    print(access_token_request.text)

def main():
    get_access_token()

if __name__ == '__main__':
    main()