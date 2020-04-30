#!/bin/python3

'''
Client ID c6b73836172b40b2ac90879f9b54271b
Client Secret bced1ccc150b4ee5b65f295b98e33b95


Notes / TO DO

Need to comment everything and make a better naming system, shit is unorganized

Need to make a tag for genre so that I don't need to make a database for each one
	Maybe change from csv to sql? Need to look into that

Need to do GUI duh

Need to make a better way to name the playlists and to handle the inputs

Need to make it so that it will run as a program, not just a single script
	Take an input, become interactive, give an option of what to do with the results
		Maybe start with just the previews of each song in the playlist?
	Once this is done I reckon it'll be easier to make the GUI

Maybe look into another audio processor so that I can use artists that are just on soundcloud
	Would need a way to make a playlist if they aren't on spotify, although more and more people are getting on spotify

Maybe look into lyrical analysis? Hmm



'''
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

	# art = recommend_artists('post malone')
	# print(art)
	# findArtistID('post malone')
	# a = {'danceability': 0.695, 'energy': 0.762, 'key': 0, 'loudness': -3.497, 'mode': 1, 'speechiness': 0.0395, 'acousticness': 0.192, 'instrumentalness': 0.00244, 'liveness': 0.0863, 'valence': 0.553, 'tempo': 120.042, 'type': 'audio_features', 'id': '21jGcNKet2qwijlDFuPiPb', 'uri': 'spotify:track:21jGcNKet2qwijlDFuPiPb', 'track_href': 'https://api.spotify.com/v1/tracks/21jGcNKet2qwijlDFuPiPb', 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/21jGcNKet2qwijlDFuPiPb', 'duration_ms': 215280, 'time_signature': 4}

	# with open('dtd.txt', 'w') as outfile:
	# 	json.dump(a, outfile, indent = 4)
	# print(a)


	token = util.prompt_for_user_token('1255728105', 'playlist-modify-public')

	if token:
		sp = spotipy.Spotify(auth=token)

		makeBigDatabase(big_artists)
		makeSmallDatabase(small_artists)

		# make_playlist('j. cole')
		# big_artist_list = []
		# with open('data.csv', newline ='') as csvfile:
		# 	reader = csv.DictReader(csvfile)
		# 	for row in reader:
		# 		big_artist_list.append(row['Big Artist'])
		#
		# tries = 0
		# match = False
		# while tries < 5 and not match:
		# 	artist_name = input("Choose an artist that you like.\n")
		# 	if artist_name in big_artist_list:
		# 		print()
		# 		print("Good choice, hang on one minute...")
		# 		print()
		# 		print("We're getting your recommended playlist now.")
		# 		print()
		# 		match = True
		# 	else:
		# 		tries += 1
		# 		print("Please try again. Tries left = ", 5-tries)
		# if tries >= 5:
		# 	print("Good-bye.")
		# else:
		# 	make_playlist(artist_name)
