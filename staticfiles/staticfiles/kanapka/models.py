from django.contrib.auth.models import User, AbstractUser
from django.db import models

# Create your models here.
from django.db.models import Count


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

    @classmethod
    def get_number_of_subscriptions_for_locations(cls):
        temp = cls.objects.all().values('places').exclude(places__isnull=True).annotate(
            total=Count('places')).order_by('total')
        number_of_subscriptions = {}
        for i in temp:
            number_of_subscriptions[i['places']] = i['total']
        return number_of_subscriptions
