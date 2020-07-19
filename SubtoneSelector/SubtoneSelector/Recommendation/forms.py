from django import forms
from django.core import validators
from Recommendation.models import BigArtist

class ArtistForm(forms.Form):
    name = forms.CharField(max_length = 64, widget=forms.TextInput(attrs={'class': 'search-form', 'placeholder': 'Artist Name'}), label= '')

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'search-form', 'placeholder': 'Enter Spotify Username'}), label= '',max_length = 64)
