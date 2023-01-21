from django.urls import path, include
from rest_framework import routers

from api.viewsets import PointValueViewSet, MeasuringDeviceViewSet
from views import index, settings

app_name = 'aquarium'

router = routers.DefaultRouter()
router.register(r'point_value', PointValueViewSet, basename='point_value')
router.register(r'measuring_device', MeasuringDeviceViewSet, basename='measuring_device')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', index, name='index'),
    path('settings/', settings, name='settings')

]