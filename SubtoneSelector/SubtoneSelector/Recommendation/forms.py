from django import forms
from django.core import validators
from Recommendation.models import BigArtist

class ArtistForm(forms.Form):
    name = forms.CharField(max_length = 64)

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 64)
