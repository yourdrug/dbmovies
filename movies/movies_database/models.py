from django.db import models

class Movie(models.Model):
    name = models.CharField(max_length=80)
    year = models.SmallIntegerField()
    country = models.CharField(max_length=80)
