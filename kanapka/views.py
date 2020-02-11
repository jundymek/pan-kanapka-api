from push_notifications.models import WebPushDevice
from rest_framework import viewsets, generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from kanapka.helpers import location_add_remove_from_subscription, is_webpushdevice_subscribed_by_user, \
    is_location_subscribed_by_user
from kanapka.models import Place, MyUser, MenuItem
from kanapka.serializers import PlaceSerializer, UserSerializer, UserDetailSerializer, MenuItemSerializer


class SuperUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        if request.method == 'POST' or request.method == 'DELETE':
            print(request.user)
            return bool(request.user.is_superuser)
        return True


# ------------------API Endpoints-------------------

@api_view(['PATCH'])
@authentication_classes((TokenAuthentication,))
def subscribe(request, place_id):
    if request.user.is_authenticated:
        user = MyUser.objects.get(id=request.user.id)
        location_add_remove_from_subscription(place_id, user)
        print(MyUser.get_number_of_subscriptions_for_locations())
        return Response({"message": "Success"})
    else:
        print('User not logged')
        return Response({"message": "User is not logged"})


class PlaceListApiView(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (SuperUserPermission,)
    serializer_class = PlaceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserApiView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = MyUser.objects.all()


class UserDetailApiView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'username'

    def get_queryset(self):
        print(f'USER: {self.request.user}')
        return MyUser.objects.filter(username=self.request.user)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
def subscribe_for_push(request):
    print(request.data)
    new_device = WebPushDevice(name=request.data['name'], active=True, registration_id=request.data['registration_id'],
                               browser=request.data['browser'], p256dh=request.data['p256dh'],
                               auth=request.data['auth'], user=request.user)
    if not WebPushDevice.objects.filter(name=request.user, registration_id=request.data['registration_id']).count():
        print('NIE ISTNIEJE')
        new_device.save()
    else:
        print('ISTNIEJE')
        print(WebPushDevice.objects.filter(name=request.user, registration_id=request.data['registration_id']))

    return Response({"message": "Push notification subscribe"})


@api_view(['GET'])
def get_number_of_subscriptions_for_locations(request):
    return Response(MyUser.get_number_of_subscriptions_for_locations())


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((SuperUserPermission,))
def send_notification_message(request, location_id):
    location = get_object_or_404(Place, id=location_id)
    users = MyUser.objects.all()
    counter = 0
    for user in users:
        if is_webpushdevice_subscribed_by_user(user.username) and is_location_subscribed_by_user(location_id,
                                                                                                 user):
            to_send = WebPushDevice.objects.get(name=user.username)
            to_send.send_message(f"Za 5 min będę: {location.address} : {location.name}")
            counter += 1
    if counter > 0:
        print(counter)
        return Response({"message": f"Message was sent to {counter} users"})
    print(counter)
    return Response({"message": "Location is not subscribed by users"})


class MenuItemsApiView(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (SuperUserPermission,)
    serializer_class = MenuItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
