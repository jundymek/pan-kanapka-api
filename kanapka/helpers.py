from kanapka.models import Place


def location_add_remove_from_subscription(place_id, user):
    if location_is_subscribed(place_id, user):
        location_to_remove = Place.objects.get(id=place_id)
        user.places.remove(location_to_remove)
        print(user.places)
    else:
        user.places.add(Place.objects.get(id=place_id))


def location_is_subscribed(place_id, user):
    subscribed_locations_ids = [x['id'] for x in user.places.values() if x['id'] == place_id]
    if place_id in subscribed_locations_ids:
        return True