from django.contrib import admin

# Register your models here.
from kanapka.models import Place, MyUser

admin.site.register(Place)
admin.site.register(MyUser)