import requests
import webbrowser
import json
from datetime import date
from urllib.parse import urlencode
import base64
from dotenv import load_dotenv
import os


load_dotenv()

clientID = os.getenv('CLIENT_ID')
clientSecret = os.getenv('CLIENT_SECRET')
encoded_credentials = base64.b64encode(clientID.encode() + b':' + clientSecret.encode()).decode("utf-8")
user_id = os.getenv('USER_ID')
discover_weekly_id = os.getenv('DISCOVER_ID')


# URLS
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'
REDIRCT_URI = 'YOUR REDIRECT URI'
PLAYLIST_URL = f"https://api.spotify.com/v1/users/{user_id}/playlists"
DISCOVER_URL = f"http://api.spotify.com/v1/playlists/{discover_weekly_id}"

class saveWeekly:
    def __init__(self):
        self.user_id = os.getenv('USER_ID')
        self.spotify_token = ''
        self.refresh_token = ''
        self.tracks = ''
        self.newPlaylist_id = ''

    def getAuthCode(self, clientID):
        # POST
        auth_code = {
            'client_id': clientID,
            'response_type': 'code',
            'redirect_uri': REDIRCT_URI,
            'scope': 'user-library-read playlist-read-private playlist-modify-public playlist-modify-private'
        }
        webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_code))

    def getAccessToken(self):
        codeLink = input('Copy and paste the link that was opened here: ')
        print(f"This is the link that was pasted: {codeLink}")
        code = codeLink.split('code=')[-1]
        access_param = {
            'grant_type' : 'authorization_code',
            'code' : code,
            'redirect_uri': REDIRCT_URI
        }

        headers = {
            'Authorization' : 'Basic ' + encoded_credentials,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(TOKEN_URL, data = access_param, headers= headers)
        self.spotify_token = response.json()['access_token']
        self.refresh_token = response.json()['refresh_token']
        if response.status_code == 200:
            print(f"The Access Token : {self.spotify_token}\nThe Refresh Token : {self.refresh_token}")
        else:
            print("Invalid Authorization Code, please makes sure you approve the use of SaveWeekly")
    def findPlaylist(self):
        print("Finding your discover weekly songs")
        headers = {
            'Content-Type' : 'applicaiton/json',
            'Authorization' : f"Bearer {self.spotify_token}"
        }

        response = requests.get(DISCOVER_URL, headers= headers)
        response_json = response.json()
        for song in response_json['tracks']["items"]:
            self.tracks += (song['track']['uri'] + ',')
        self.tracks = self.tracks[:-1]
        if response.status_code == 200:
            print('Found playlist!')
            self.addToPlaylist()
        elif response.status_code == 401:
            print("Unable to find playlist token has expired or revoked")
        elif response.status_code == 403:
            print('Bad OAuth request')
        else:
            print('The app has exceeded its rate limits.')
    
    def createPlaylist(self):
        print('Creating playlist...')
        today = date.today()
        playlist_data = json.dumps({
            'name' : f"{today}'s Discover Weekly",
            'description' : 'Discover weekly recorded by SaveWeekly Bot',
            'public' : False
        })
        headers = {
            'Content-Type' : 'applicaiton/json',
            'Authorization' : f"Bearer {self.spotify_token}"
        }
        response = requests.post(PLAYLIST_URL, data = playlist_data, headers = headers)
        if response.status_code == 201:
            print('Created playlist!')
        elif response.status_code == 401:
            print("Unable to find playlist token has expired or revoked")
        elif response.status_code == 403:
            print('Bad OAuth request')
        else:
            print('The app has exceeded its rate limits.')
        return response.json()['id']
    
    def addToPlaylist(self):
        print("Adding songs...")
        self.newPlaylist_id = self.createPlaylist()
        NEWPLAYLIST_URL = f"https://api.spotify.com/v1/playlists/{self.newPlaylist_id}/tracks?uris={self.tracks}"
        headers = {
            'Content-Type' : 'applicaiton/json',
            'Authorization' : f"Bearer {self.spotify_token}"
        }
        response = requests.post(NEWPLAYLIST_URL, headers = headers)
        if response.status_code == 201:
            print("Added Songs!")
        elif response.status_code == 401:
            print("Unable to find playlist token has expired or revoked")
        elif response.status_code == 403:
            print('Bad OAuth request')
        else:
            print('The app has exceeded its rate limits.')


    def refreshAccessToken(self):
        refresh_data = {
            'grant_type' : 'refresh_token',
            'refresh_token' : self.refresh_token
        }
        headers = {
            'Authorization' : 'Basic ' + encoded_credentials,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(TOKEN_URL, data = refresh_data, headers = headers)
        self.spotify_token = response.json()['access_token']
        if response.status_code == 200:
            print('Token has been refreshed')
        else:
            print('Token failed to refresh')
if __name__ == '__main__':
    s = saveWeekly()
    s.getAuthCode(clientID)
    s.getAccessToken()
    s.findPlaylist()


