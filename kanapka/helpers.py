from push_notifications.models import WebPushDevice

from kanapka.models import Place


def location_add_remove_from_subscription(place_id, user):
    if is_location_subscribed_by_user(place_id, user):
        location_to_remove = Place.objects.get(id=place_id)
        user.places.remove(location_to_remove)
    else:
        user.places.add(Place.objects.get(id=place_id))


def is_webpushdevice_subscribed_by_user(username):
    subscribed_devices_by_username = [device['name'] for device in WebPushDevice.objects.all().values()]
    return username in subscribed_devices_by_username


def is_location_subscribed_by_user(location_id, user):
    return location_id in [location['id'] for location in user.places.values()]
