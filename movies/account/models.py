from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    image = models.ImageField(upload_to="user")


class OnlineAccount(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.username
