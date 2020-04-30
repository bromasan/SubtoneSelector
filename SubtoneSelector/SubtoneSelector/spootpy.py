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


from Recommendation.models import BigArtist, SmallArtist

def makeBigDatabase(artists):
	data_set = {}
	data_set['artists'] = []
	for artist_name in artists:
		results = sp.search(q=artist_name, limit=50)
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


		avgData['artist'] = artist_name
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
		artst = BigArtist.objects.update_or_create(name = artist['artist'], defaults = vals)[0]

def makeSmallDatabase(artists):
	data_set = {}
	data_set['artists'] = []
	for artist_name in artists:
		results = sp.search(q=artist_name, limit=50)
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


		avgData['artist'] = artist_name
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






if __name__=='__main__':
	big_artists = ['Post Malone', 'Khalid', 'Drake', 'Lil Nas X', 'Travis Scott', 'Juice WRLD', 'DaBaby', 'Cardi B', 'Lil Baby', 'Meek Mill', 'A Boogie Wit Da Hoodie', 'Lizzo', '21 Savage', 'XXXTentacion', 'Chris Brown', 'Kodak Black', 'Gunna', 'J. Cole', 'Young Thug', 'Lil Tecca']
	small_artists = ['Lil Keed', 'Pop Smoke', 'Guapdad 4000', 'Jack Harlow', 'Kaash Paige', 'Baby Keem', 'Arizona Zervas', 'Layton Greene', 'King Von', 'Don Toliver', 'Fivio Foreign', 'Arin Ray', 'Trevor Daniel', 'Stunna 4 Vegas', 'YNW Melly', 'Polo G', 'Roddy Rich', 'Lil Tjay', 'YBN Cordae', 'Lil Mosey', 'YBN Nahmir', 'Flipp Dinero', 'Saweetie', 'Yung Bans', 'Young Nudy', 'Tierra Whack', 'Noname', 'Asian Doll', 'Kid Trunks']

	token = util.prompt_for_user_token('1255728105', 'playlist-modify-public')

	if token:
		sp = spotipy.Spotify(auth=token)

		makeBigDatabase(big_artists)
		makeSmallDatabase(small_artists)

		
