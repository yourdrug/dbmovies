from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=80)
    year = models.SmallIntegerField()
    country = models.CharField(max_length=80)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Id {self.id}: {self.name} {self.year}'
