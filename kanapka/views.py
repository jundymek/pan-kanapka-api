from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Count
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView
from push_notifications.models import WebPushDevice
from rest_framework import viewsets, generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, api_view
from rest_framework.response import Response

from kanapka.forms import CustomUserCreationForm
from kanapka.helpers import location_add_remove_from_subscription
from kanapka.models import Place, MyUser
from kanapka.serializers import PlaceSerializer, UserSerializer, UserDetailSerializer


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        new_user = form.save()
        print(new_user)
        login(self.request, new_user)
        return valid


@api_view(['PATCH'])
@authentication_classes((TokenAuthentication,))
def subscribe(request, place_id):
    if request.user.is_authenticated:
        user = MyUser.objects.get(id=request.user.id)
        location_add_remove_from_subscription(place_id, user)
        return Response({"message": "Success"})
    else:
        print('User not logged')
        return Response({"message": "User is not logged"})


# @api_view(['POST'])
# @permission_classes((IsAdminUser,))
# @permission_classes([IsAuthenticated])
# def add_new_place(request):
#     try:
#         if request.method == "POST":
#             name = request.POST['name']
#             address = request.POST['address']
#             latitude = request.POST['latitude']
#             longitude = request.POST['longitude']
#             new_place = Place(name=name, address=address, latitude=latitude, longitude=longitude)
#             new_place.save()
#             return Response({"message": "New location was added"})
#     except:
#         return Response({"message": "Something went wrong"})


class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "places"

    def get_queryset(self):
        return Place.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        places = [{'id': place.id, 'name': place.name, 'address': place.address, 'latitude': place.latitude,
                   'longitude': place.longitude} for place in Place.objects.all()]
        print(places)
        context['places'] = places
        return context


class PlaceDeleteView(DeleteView):
    model = Place
    success_url = reverse_lazy('index')

    def get(self, *args, **kwargs):
        message = f'{self.get_object().name} was deleted'
        messages.success(self.request, message)
        return self.post(*args, **kwargs)


class SuperUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        if request.method == 'POST' or request.method == 'DELETE':
            print(request.user)
            return bool(request.user.is_superuser)
        return True


# ------------------API Endpoints-------------------
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


class PlaceDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()
    permission_classes = (SuperUserPermission,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(self.get_object())
        self.perform_destroy(instance)
        return Response(f'Removed: {serializer.data}', status=status.HTTP_200_OK)


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
