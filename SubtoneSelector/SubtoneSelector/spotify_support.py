from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import oauth2
import spotipy
import time
import sys
import spotipy.util as util
import pandas as pd
import sqlite3
from django_pandas.io import read_frame
import urllib.request


SPOTIPY_REDIRECT_URI = ''

SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
CACHE_PATH = '.cache'
token=''
username=''

sp_oauth = spotipy.SpotifyOAuth(
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    SPOTIPY_REDIRECT_URI,
    scope='playlist-modify-public',
    cache_path=CACHE_PATH,
    show_dialog=False
)

#return the current global token
def get_token():
    return token

#checks if there is token information stored for current user.
# if so, set the token to the value stored in 'access_token'
# otherwise, return the authorization link so the user can log in with their Spotify account
def login_spotify(user):

    global token, username
    username = user
    sp_oauth.cache_path = '.cache_' + username

    token_info = sp_oauth.get_cached_token()

    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        return auth_url
    else:
        token = token_info['access_token']

    return

# Once the user authorizes Spotify access it will redirect to "/logged/" where auth_handler 
# will be called. This parses the URL for the access token information, then sets the token
def auth_handler(request):
    code = sp_oauth.parse_response_code(request)
    token_info = sp_oauth.get_access_token(code)
    global token
    token = token_info['access_token']

# Takes the name of the new artist and finds tracks by said artist where the audio features
# most closely correlate with the average audio features of the artist
# Tries to find songs that most likely represents the artist's sound
# Returns 5 song URIs in a list
def findTrackCorr( artist_name, sp):
    conn =sqlite3.connect('db.sqlite3')
    results = sp.search(q=artist_name, limit=5)
    tids = []

    for i, t in enumerate(results['tracks']['items']):
        tids.append(t['uri'])

    data = {}
    unincluded = ['analysis_url', 'duration_ms', 'time_signature', 'track_href', 'type', 'uri']
    features = sp.audio_features(tids)

    for feature in features:
        for key in feature:
            if key not in unincluded:
                if key not in data:
                    data[key] = [feature[key]]
                else:
                    data[key].append(feature[key])

    small_df = pd.read_sql_query("SELECT * FROM recommendation_smallartist", conn)
    small_artist_matrix = small_df.pivot_table(columns = 'name')

    df = pd.DataFrame.from_dict(data)
    track_matrix = df.pivot_table(columns='id')

    artist = small_artist_matrix[artist_name]

    similar_to_artist = track_matrix.corrwith(artist)
    similar_to_artist.head()

    corr_artist = pd.DataFrame(similar_to_artist, columns=['correlation'])
    corr_artist.dropna(inplace=True)

    corr_artist = corr_artist.sort_values(by='correlation', ascending=False)
    corr_artist.head()
    count = 0
    track_list = []
    repeats = []
    for index, row in corr_artist.iterrows():
        if count < 6:
            track_name = sp.track(row.name)['name']
            if track_name in repeats:
                continue
            else:
                repeats.append(track_name)
                #track_artist = sp.track(row.name)['artists'][0]['name']
                #track_url = "spotify:track:"+row.name
                track_list.append(row.name)
                count += 1
        else:
            break
    return track_list

# Takes in the Big Artist that the user selected, and the recommended artists discovered in recommend_artists()
# Calls findTrackCorr() to find the songs for each of the recommended artists
# Connects to user's account and makes a playlist with each of the songs
# Returns the link for the playlist
def make_playlist(artist, new_artists):

    sp = spotipy.Spotify(auth=token)

    playlist_name = "Subtone Playlist: " + artist

    sp.user_playlist_create(username, playlist_name, public=True, description="")

    playlist_id = ''

    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            if playlist['name'] == playlist_name:
                playlist_id = playlist['id']

    playlist = []



    for key in new_artists:
        playlist.extend(findTrackCorr(key, sp))

    sp.user_playlist_add_tracks(username, playlist_id, playlist, position=None)

    playlist_URL = "https://open.spotify.com/playlist/" + playlist_id

    return playlist_URL

# Takes in the artist user selects
# Uses the stored artists data of the artist to find the new artists that most closely relate to input artist
# Returns a list of all of the new artists
def recommend_artists( artist_name):

    sp = spotipy.Spotify(auth=token)

    conn =sqlite3.connect('db.sqlite3')
    big_df =pd.read_sql_query("SELECT *  FROM recommendation_bigartist WHERE name ='"+artist_name+"'", conn)
    small_df =pd.read_sql_query("SELECT * FROM recommendation_smallartist", conn)

    big_artist_matrix = big_df.pivot_table(columns = 'name')
    small_artist_matrix = small_df.pivot_table(columns = 'name')

    artist = big_artist_matrix[artist_name]

    similar_to_artist = small_artist_matrix.corrwith(artist, axis=0)

    corr_artist = pd.DataFrame(similar_to_artist, columns=['correlation'])
    corr_artist = corr_artist.sort_values(by='correlation', ascending=False)

    count = 0
    artist_list = []
    for index, row in corr_artist.iterrows():
        if count > 0 and count < 6:
            artist_list.append(row.name)
        count += 1

    return artist_list

# Takes in an artist name
# Finds Spotify image for artist
# Returns the image URL to later be displayed on page
def get_image(artist_name):

    sp = spotipy.Spotify(auth=token)

    results = sp.search(q='artist:' + artist_name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
    	return items[0]['images'][0]['url']
    	# urllib.request.urlretrieve(img, 'post_malone.jpg')
    else:
    	return None

    
# Take in an artist name
# Finds the Spotify URL for artist
# Returns URL to later link user to the artist
def get_url(artist_name):

    sp = spotipy.Spotify(auth=token)

    results = sp.search(q='artist:' + artist_name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
    	return items[0]['external_urls']['spotify']
    	# urllib.request.urlretrieve(img, 'post_malone.jpg')
    else:
    	return None
