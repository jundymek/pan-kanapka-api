from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from kanapka.models import Place


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
        places = [{'id': place.id, 'name': place.name, 'address': place.address, 'latitude': place.latitude, 'longitude': place.longitude} for place in Place.objects.all()]
        print(places)
        context['places'] = places
        return context


