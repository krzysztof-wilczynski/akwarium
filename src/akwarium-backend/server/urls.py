from django.urls import re_path, include

urlpatterns = [
    re_path(r'^api/', include('aquarium.api.urls', namespace='aquarium'))
]
