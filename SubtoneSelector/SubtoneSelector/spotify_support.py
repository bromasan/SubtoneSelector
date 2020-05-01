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


SPOTIPY_REDIRECT_URI = 'http://bromasan.pythonanywhere.com/logged/'

SPOTIPY_CLIENT_ID = 'c6b73836172b40b2ac90879f9b54271b'
SPOTIPY_CLIENT_SECRET = 'bced1ccc150b4ee5b65f295b98e33b95'
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

def get_token():
    return token

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


def auth_handler(request):
    code = sp_oauth.parse_response_code(request)
    token_info = sp_oauth.get_access_token(code)
    global token
    token = token_info['access_token']



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
                track_artist = sp.track(row.name)['artists'][0]['name']
                track_url = "spotify:track:"+row.name
                # track_list.append(track_artist)
                track_list.append(row.name)
                count += 1
        else:
            break
    return track_list

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

    print("Follow this link to visit your new playlist:")
    print(playlist_URL)

    return playlist_URL

def recommend_artists( artist_name):

    sp = spotipy.Spotify(auth=token)

    conn =sqlite3.connect('db.sqlite3')
    # read in the info for big artists into DataFrame
    big_df =pd.read_sql_query("SELECT *  FROM recommendation_bigartist WHERE name ='"+artist_name+"'", conn)

    # read in the info for small artists into DataFrame
    small_df =pd.read_sql_query("SELECT * FROM recommendation_smallartist", conn)


    # make big artist matrix to hold data
    big_artist_matrix = big_df.pivot_table(columns = 'name')

    # make small artist matrix to hold data
    small_artist_matrix = small_df.pivot_table(columns = 'name')

    # makes a table object for just the subject
    artist = big_artist_matrix[artist_name]


    # find table of artists that most closely correlate with subject
    similar_to_artist = small_artist_matrix.corrwith(artist, axis=0)

    #makes table of similar_to_artist with correlation value
    corr_artist = pd.DataFrame(similar_to_artist, columns=['correlation'])
    # corr_artist.dropna(inplace=True)

    # sorts table by corr values
    corr_artist = corr_artist.sort_values(by='correlation', ascending=False)

    count = 0
    artist_list = []
    for index, row in corr_artist.iterrows():
        if count > 0 and count < 6:
            artist_list.append(row.name)
        count += 1

    return artist_list

def get_image(artist_name):

    sp = spotipy.Spotify(auth=token)

    results = sp.search(q='artist:' + artist_name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
    	return items[0]['images'][0]['url']
    	# urllib.request.urlretrieve(img, 'post_malone.jpg')
    else:
    	return None

def get_url(artist_name):

    sp = spotipy.Spotify(auth=token)

    results = sp.search(q='artist:' + artist_name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
    	return items[0]['external_urls']['spotify']
    	# urllib.request.urlretrieve(img, 'post_malone.jpg')
    else:
    	return None
