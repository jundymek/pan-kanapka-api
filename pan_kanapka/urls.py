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
from django.conf.urls.static import static
from django.urls import path, include
from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet, GCMDeviceAuthorizedViewSet
from rest_framework import routers

from kanapka import views
from pan_kanapka import settings

router = routers.DefaultRouter()
router.register('places', views.PlaceListApiView)
router.register('menu_items', views.MenuItemsApiView)
router.register('users', views.UserApiView)
router.register('device/apns', APNSDeviceAuthorizedViewSet)
router.register('device/gcm', GCMDeviceAuthorizedViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('subscribe/<int:place_id>/', views.subscribe, name='subscribe'),
    path('subscribe_for_push/', views.subscribe_for_push, name="subscribe_for_push"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls)),
    path('api/user/<str:username>/', views.UserDetailApiView.as_view()),
    path('api/get_number_of_subscriptions/', views.get_number_of_subscriptions_for_locations,
         name="get_number_of_subscriptions"),
    path('api/send_notification/<int:location_id>', views.send_notification_message, name="send_notification"),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)