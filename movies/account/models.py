from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    image = models.ImageField(upload_to="user/")
    is_critic = models.BooleanField(default=False)


class OnlineAccount(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.username


class Guest(models.Model):
    name = models.CharField(default="Guest")

    def __str__(self):
        return self.name
