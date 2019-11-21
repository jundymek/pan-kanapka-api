"""pan_kanapka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from kanapka import views
from kanapka.views import IndexView, PlaceDeleteView, SignUpView

router = routers.DefaultRouter()
router.register('places', views.PlaceApiView, base_name='places')
router.register('users', views.UserApiView, base_name='users')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('add/', views.add_new_place, name='add'),
    path('delete/<int:pk>/', PlaceDeleteView.as_view(), name='delete'),
    path('subscribe/<int:placeId>/', views.subscribe, name='subscribe'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', SignUpView.as_view(), name="signup"),
    path('api/', include(router.urls)),

]
