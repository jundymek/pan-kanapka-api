from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView
from rest_framework import viewsets

from kanapka.forms import CustomUserCreationForm
from kanapka.models import Place, MyUser
from kanapka.serializers import PlaceSerializer


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


def subscribe(request, placeId):
    print(placeId)
    user = MyUser.objects.get(id=request.user.id)
    user.places.add(Place.objects.get(id=placeId))
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
class PlaceApiView(viewsets.ModelViewSet):
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()
