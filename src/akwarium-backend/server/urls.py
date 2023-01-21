from django.contrib import admin
from django.urls import re_path, include
from aquarium.tasks import startup

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include('aquarium.api.urls', namespace='aquarium'))
]

# https://stackoverflow.com/a/6792076
startup.delay()
