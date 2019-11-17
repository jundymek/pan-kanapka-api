from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from kanapka.models import Place


class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "places"

    def get_queryset(self):
        return Place.objects.all()
