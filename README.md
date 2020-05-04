# SubtoneSelector

SubtoneSelector is an application geared towards finding users new artists based off an artist that the user likes. The idea is to use Spotify's API to grab audio features of an artists songs, then calculating their "Average Sound". Once this is found, five artists are found that are not well known but correlate to the original artist's sound. A playlist is then created on the user's account that contains 5 songs from the new artist under the name Subtone Selector: {Original Artist}.

## Getting Started


### Prerequisites

Will need to download latest Django, Python, Pandas, Spotipy, Django-Pandas, Django-Bootstrap4. These will also install several other packages.

Use pip:

```
pip install module
```


### Installing

Before installation, you will be required to get a Client ID from Spotify's Developers site. Register your app and save the Client ID and Client Secret -- you will need these. Then set your Redirect URI to 'http://localhost:8000/logged/', or a port of your choosing, if you want to run it locally. 

Next, download this repository.

Most of your changes will need to be made in spotify_support.py



Set your registered app information:

```
SPOTIPY_REDIRECT_URI = 'your redirect URI'
SPOTIPY_CLIENT_ID = 'your client id'
SPOTIPY_CLIENT_SECRET = 'your client secret'
```

In SubtoneSelector/settings.py, set your secret key to a 
```
SECRET_KEY = 'your secret key'
```

Next you'll want to make the necessary migrations to create your database.
```
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
```

Next, you can edit the .csv files to contain your own artists (my examples may be lacking at the moment), or keep them the same. Run spootpy.py to populate your databases.
```
python spootpy.py
```

You'll then want to create a superuser so that you can access the admin side of the app.
```
python manage.py createsuperuser
```

Finally, you can run the application and visit the link your command line provides. 
```
python manage.py runserver
```

Side note, when developing this, I used miniconda and created an enviroment so that my computer's packages wouldn't interfere with this. This might be a good idea!

Enjoy and please leave feedback - there's a lot I need to update so any thoughts would be great.


## Future Changes
There are going to be plenty of changes as time permits. Some, if curious:
* More efficient means of populating database
* More reactive Front-End
* More options to create the playlist such as multiple input artists, mood, etc. 
* Better way of calculating the data points



## Acknowledgments

* All of this started when I stumbled upon this awesome article by Derrick Mwiti:
  https://towardsdatascience.com/how-to-build-a-simple-recommender-system-in-python-375093c3fb7d

