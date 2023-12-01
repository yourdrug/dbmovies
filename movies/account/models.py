from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    image = models.ImageField(upload_to="user")
