from django.contrib.auth.models import User, AbstractUser
from django.db import models


# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()


class MyUser(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    places = models.ManyToManyField(Place)
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

