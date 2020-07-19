from django.db import models
from django.http import HttpResponse, HttpResponseRedirect


# Create your models here.
class BigArtist(models.Model):
    name = models.CharField(max_length = 64)
    genre1 = models.CharField(max_length = 64)
    genre2 = models.CharField(max_length = 64)
    genre3 = models.CharField(max_length = 64)
    danceability = models.DecimalField(max_digits = 10, decimal_places = 7)
    energy = models.DecimalField(max_digits = 10, decimal_places = 7)
    key = models.DecimalField(max_digits = 10, decimal_places = 7)
    loudness = models.DecimalField(max_digits = 10, decimal_places = 7)
    mode = models.DecimalField(max_digits = 10, decimal_places = 7)
    speechiness = models.DecimalField(max_digits = 10, decimal_places = 7)
    acousticness = models.DecimalField(max_digits = 10, decimal_places = 7)
    instrumentalness = models.DecimalField(max_digits = 10, decimal_places = 7)
    liveness = models.DecimalField(max_digits = 10, decimal_places = 7)
    valence = models.DecimalField(max_digits = 10, decimal_places = 7)
    tempo = models.DecimalField(max_digits = 10, decimal_places = 7)

    def __str__(self):
        return self.name



class SmallArtist(models.Model):
    name = models.CharField(max_length = 64)
    genre1 = models.CharField(max_length = 64)
    genre2 = models.CharField(max_length = 64)
    genre3 = models.CharField(max_length = 64)
    danceability = models.DecimalField(max_digits = 10, decimal_places = 7)
    energy = models.DecimalField(max_digits = 10, decimal_places = 7)
    key = models.DecimalField(max_digits = 10, decimal_places = 7)
    loudness = models.DecimalField(max_digits = 10, decimal_places = 7)
    mode = models.DecimalField(max_digits = 10, decimal_places = 7)
    speechiness = models.DecimalField(max_digits = 10, decimal_places = 7)
    acousticness = models.DecimalField(max_digits = 10, decimal_places = 7)
    instrumentalness = models.DecimalField(max_digits = 10, decimal_places = 7)
    liveness = models.DecimalField(max_digits = 10, decimal_places = 7)
    valence = models.DecimalField(max_digits = 10, decimal_places = 7)
    tempo = models.DecimalField(max_digits = 10, decimal_places = 7)

    def __str__(self):
        return self.name
