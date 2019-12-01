from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView
from rest_framework import viewsets, generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, api_view

from kanapka.forms import CustomUserCreationForm
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
def subscribe(request, placeId):
    print(placeId)
    print(request.user)
    if request.user.is_authenticated:
        print('UDAŁO SIe')
        user = MyUser.objects.get(id=request.user.id)
        user.places.add(Place.objects.get(id=placeId))
        return HttpResponseRedirect('/')
    else:
        print('User not logged')
        return HttpResponseRedirect('/')


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

    def get_queryset(self):
        print(self.request.user)
        return MyUser.objects.filter(username=self.request.user)

# class UserDetailApiView(APIView):
#     # serializer_class = UserDetailSerializer
#     # queryset = MyUser.objects.all()
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get(self, request):
#         serializer = UserSerializer(request.user)
#         return Response(serializer.data)
#
#     def put(self, request):
#         serializer = UserSerializer(request.user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
