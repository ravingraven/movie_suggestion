from django.db import models
from django.contrib.auth.models import User

class Suggestion(models.Model):
    name = models.CharField(max_length=200) # This is effectively the title
    video = models.CharField(max_length=200)
    rated = models.CharField(max_length=200)
    released = models.CharField(max_length=200)
    runtime = models.CharField(max_length=200)
    genres = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    writer = models.CharField(max_length=200)
    actors = models.CharField(max_length=1000)
    plot = models.CharField(max_length=2000)
    languages = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    awards = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Preference(models.Model):
    PREFERENCES = (('0', 'none'), ('1', 'like'), ('-1', 'dislike'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    video = models.CharField(max_length=200)
    preference = models.CharField(max_length=1, choices=PREFERENCES)

    def __str__(self):
        return self.name 
