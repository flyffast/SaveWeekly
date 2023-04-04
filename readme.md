# SaveWeekly
SaveWeekly utilizies Spotify's API to create a copy of your Discover Weekly Songs.

## Setup
### (1) Install dependencies
```bash
pip install -r requirements.txt
```
### (2) Spotify API Credentials
1. Open ```.env``` file on your local machine.
2. Sign into your [Spotify API Dashboard](https://developer.spotify.com/dashboard) and create a new application. You must fill out the box **Redirect URI**, and you can use any uri for the redirect uri (Example: ```http://localhost:8888/callback```, this is the base uri you will be redirected to once you have authorized the application to access your account. If you see "INVALID_CLIENT: Invalid redirect URI", then you have not added or used a valid uri as your redirect uri.
3. On line 24 on ```main.py``` please replace 'YOUR REDIRECT URI' with your URI that you used for step 2. 
```python
REDIRECT_URI = 'http://yoururihere'
``` 
5. Fill out the .env file with the your Client ID, Client Secret details, Username located on your [Spotify Account Overview](https://www.spotify.com/account) and your Discover Weekly Playlist ID. To locate your Discover Weekly Playlist ID, get the link to the playlist and the code will be here. ```https://open.spotify.com/playlist/youridhere?...``` Then save this file. **DO NOT SHARE THIS INFORMATION ANYHWERE PUBLICALLY**

Example:

```python
CLIENT_ID = yourid
CLIENT_SECRET = yoursecret
USER_ID = yourusername
DISCOVER_ID = yourdiscoverplaylistid
```
4. Execute main.py and open the URL genereated in your browswer.
5. Authorize your app to access your Spotify account, this will then redirect you to your Redirect URI with a brand new url.
6. Copy the whole url you were redirected to and paste the link into the console and hit enter, this will then create an authorization token as well as a refresh token. **Do not post your refresh token anywhere publically**

```
$python main.py

Copy and paste the link that was opened here:
> https://somelink.url/here?code=codehere

Created Auth Token and Refresh Token
```
## Contributing
Pull requests are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/)
