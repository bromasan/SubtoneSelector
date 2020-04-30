from django.shortcuts import render, redirect
from Recommendation.models import BigArtist
from . import forms
from django.http import HttpResponse, HttpResponseRedirect
import spotify_support


def index(request):
    token = spotify_support.get_token()
    return render(request, 'Recommendation/index.html', {'token':token})

def login(request):
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            auth_url = spotify_support.login_spotify(username)
            if auth_url:
                return redirect(auth_url)
            else:
                return redirect('search')
    return render(request, 'Recommendation/login.html', {'form':form})

def login_auth(request):
    url = request.get_full_path()
    token_info = spotify_support.auth_handler(url)
    form = forms.ArtistForm()
    return redirect('search')

def artist_form_view(request):
    form = forms.ArtistForm()
    if request.method == 'POST':
        form = forms.ArtistForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            try:
                new_artists = spotify_support.recommend_artists(name)
                new_images = []
                for i in new_artists:
                    new_images.append([i, spotify_support.get_image(i), spotify_support.get_url(i)])
                playlist = spotify_support.make_playlist(name, new_artists)
                artist_view = {
                    'playlist': playlist,
                    'new_artists': new_images
                }

                return render(request, 'Recommendation/artist.html', context=artist_view)
            except BigArtist.DoesNotExist:
                print("PERSON DOES NOT EXIST")
    return render(request, 'Recommendation/form.html', {'form':form})
