#!/bin/python3
from __future__ import print_function    # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import time
import sys
import csv
import spotipy.util as util
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SubtoneSelector.settings')

import django
django.setup()

SPOTIPY_REDIRECT_URI = ''
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
CACHE_PATH = ''
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

from Recommendation.models import BigArtist, SmallArtist

# Takes in Big Artist list 
# Connects to the Spotify and searches 50 songs from artist
# Averages the values from each song to find the average sound of an artist
# Creates a BigArtist object that contains the average data points
def makeBigDatabase(artists):
	data_set = {}
	data_set['artists'] = []
	for artist_name in artists:
		results = sp.search(q='"'+artist_name[0]+'"', limit=50)
		tids = []
		for i, t in enumerate(results['tracks']['items']):
		    tids.append(t['uri'])

		avgData = {}
		data = {}
		data['tracks'] = []
		unincluded = ['analysis_url', 'duration_ms', 'id', 'time_signature', 'track_href', 'type', 'uri']
		start = time.time()
		features = sp.audio_features(tids)
		if features == None:
			continue
		delta = time.time() - start
		for feature in features:
			td = {}
			if feature:
				for key in feature:
					if key not in unincluded:
						td[key] = feature[key]
						if key not in avgData:
							avgData[key] = feature[key]
						else:
							avgData[key] += feature[key]
				data['tracks'].append(td)

		for key in avgData:
			avgData[key] /= len(features)


		avgData['artist'] = artist_name[0]
		avgData['genre'] = artist_name[1]
		data_set['artists'].append(avgData)

	for artist in data_set['artists']:
		vals = {
			'name':artist['artist'],
			'genre':artist['genre'],
			'danceability':artist['danceability'],
			'energy':artist['energy'],
			'key':artist['key'],
			'loudness':artist['loudness'],
			'mode':artist['mode'],
			'speechiness':artist['speechiness'],
			'acousticness':artist['acousticness'],
			'instrumentalness':artist['instrumentalness'],
			'liveness': artist['liveness'],
			'valence':artist['valence'],
			'tempo':artist['tempo']
		}
		artst = BigArtist.objects.update_or_create(name = artist['artist'], defaults = vals)[0]

# Takes in Small Artist list 
# Connects to the Spotify and searches 50 songs from artist
# Averages the values from each song to find the average sound of an artist
# Creates a SmallArtist object that contains the average data points
def makeSmallDatabase(artists):
	data_set = {}
	data_set['artists'] = []
	for artist_name in artists:
		results = sp.search(q='"'+artist_name[0]+'"', limit=50)
		tids = []
		for i, t in enumerate(results['tracks']['items']):
		    tids.append(t['uri'])

		avgData = {}
		data = {}
		data['tracks'] = []
		unincluded = ['analysis_url', 'duration_ms', 'id', 'time_signature', 'track_href', 'type', 'uri']
		start = time.time()
		features = sp.audio_features(tids)
		if features == None:
			continue
		delta = time.time() - start
		for feature in features:
			td = {}
			if feature:
				for key in feature:
					if key not in unincluded:
						td[key] = feature[key]
						if key not in avgData:
							avgData[key] = feature[key]
						else:
							avgData[key] += feature[key]
				data['tracks'].append(td)

		for key in avgData:
			avgData[key] /= len(features)


		avgData['artist'] = artist_name[0]
		avgData['genre'] = artist_name[1]
		data_set['artists'].append(avgData)

	for artist in data_set['artists']:
		vals = {
			'name':artist['artist'],
			'genre':"Hip Hop",
			'danceability':artist['danceability'],
			'energy':artist['energy'],
			'key':artist['key'],
			'loudness':artist['loudness'],
			'mode':artist['mode'],
			'speechiness':artist['speechiness'],
			'acousticness':artist['acousticness'],
			'instrumentalness':artist['instrumentalness'],
			'liveness': artist['liveness'],
			'valence':artist['valence'],
			'tempo':artist['tempo']
		}
		artst = SmallArtist.objects.update_or_create(name = artist['artist'], defaults = vals)[0]





# Main code that opens a big_artist.csv file and small_artist.csv file 
# Adds the artists in the files to the respective lists
# Calls the respective functions to create/update the Big and Small Artist databases
if __name__=='__main__':
	big_artists = []
	small_artists = []

	with open('big_artists.csv', newline ='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			big_artists.append([row['artist'], row['genre']])
	with open('small_artists.csv', newline ='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			small_artists.append([row['artist'], row['genre']])

	

		client_credentials_manager = SpotifyClientCredentials(client_id = SPOTIPY_CLIENT_ID, client_secret =SPOTIPY_CLIENT_SECRET)
		sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

		makeBigDatabase(big_artists)
		makeSmallDatabase(small_artists)

		
