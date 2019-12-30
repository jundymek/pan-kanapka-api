from django.test import TestCase

from kanapka.models import MyUser
from kanapka.models import Place
from .helpers import is_location_subscribed_by_user, location_add_remove_from_subscription


# Create your tests here.
class HelpersSubscriptionsTestCase(TestCase):
    def setUp(self):
        MyUser.objects.create(username="user1")
        user1 = MyUser.objects.get(username="user1")
        place1 = Place.objects.create(name="test1", address="adres_test", latitude=10, longitude=11)
        user1.places.add(place1)

    def test_location_is_subscribed_by_user(self):
        user1 = MyUser.objects.get(id=1)
        self.assertEqual(is_location_subscribed_by_user(1, user1), True)

    def test_location_is_not_subscribed_by_user(self):
        user1 = MyUser.objects.get(id=1)
        self.assertEqual(is_location_subscribed_by_user(111, user1), False)

    def test_location_removed_from_subscription(self):
        user1 = MyUser.objects.get(id=1)
        location_add_remove_from_subscription(1, user1)
        self.assertEqual(user1.places.count(), 0)

    def test_location_add_to_subcription(self):
        user1 = MyUser.objects.get(id=1)
        Place.objects.create(name="test2", address="adres_test2", latitude=10, longitude=11)
        location_add_remove_from_subscription(2, user1)
        self.assertEqual(user1.places.count(), 2)
