from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView

from kanapka.forms import CustomUserCreationForm
from kanapka.models import Place


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = form.save()
        print(new_user)
        login(self.request, new_user)
        return valid


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


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
