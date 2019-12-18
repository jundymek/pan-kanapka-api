from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView
from push_notifications.models import GCMDevice, WebPushDevice
from rest_framework import viewsets, generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, api_view

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


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def subscribe_api(request):
    print(request.user)
    if request.user.is_authenticated:
        fcm_device = GCMDevice.objects.create(
            registration_id="eiGO0YLDDmk:APA91bHtZZPNI8jxcyP2M4utAUplQ3hmpJZkvk…Wjfm2_TKmBsp13Hxg92C-oAL9sFzbcM8ujfz2sCEAYRdoJxkT",
            cloud_message_type="FCM", user=request.user)
        print(GCMDevice.objects.all().values)
        print(fcm_device)
        fcm_device.send_message("This is a message")
        return HttpResponseRedirect('/')
    else:
        print('User not logged')
        return HttpResponseRedirect('/')


@api_view(['PATCH'])
@authentication_classes((TokenAuthentication,))
def subscribe(request, place_id):
    if request.user.is_authenticated:
        user = MyUser.objects.get(id=request.user.id)
        location_add_remove_from_subscription(place_id, user)
        from rest_framework.response import Response
        return Response({"message": "Success"})
    else:
        print('User not logged')
        return Response({"message": "Success"})


def add_new_place(request):
    try:
        if request.method == "POST":
            name = request.POST['name']
            address = request.POST['address']
            latitude = request.POST['latitude']
            longitude = request.POST['longitude']
            new_place = Place(name=name, address=address, latitude=latitude, longitude=longitude)
            new_place.save()
            return HttpResponseRedirect('/')
    except:
        return HttpResponseRedirect('/')


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


# ------------------API Endpoints-------------------
class PlaceListApiView(viewsets.ModelViewSet):
    # serializer_class = PlaceSerializer
    queryset = Place.objects.all()
    authentication_classes = (TokenAuthentication,)

    def get_serializer(self, *args, **kwargs):
        if self.request.user and self.request.user.is_authenticated:
            serializer_class = PlaceSerializer
            print(self.request.user)
        else:
            print(self.request.user)
            serializer_class = PlaceSerializer
            # serializer_class = UnauthenticadedPlaceSerializer
        return serializer_class(*args, **kwargs)


class PlaceDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()


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
    if not WebPushDevice.objects.filter(user=request.user, registration_id=request.data['registration_id']).count():
        print('NIE ISTNIEJE')
        new_device.save()
    else:
        print('ISTNIEJE')

    return HttpResponseRedirect('/')
