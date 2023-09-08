from django.db import models

class Movie(models.Model):
    name = models.CharField(max_length=80)
    year = models.IntegerField(max_length=4)
    country = models.CharField(max_length=80)
