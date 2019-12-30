from django import forms
from django.contrib.auth.forms import UserCreationForm

from kanapka.models import MyUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username',)
