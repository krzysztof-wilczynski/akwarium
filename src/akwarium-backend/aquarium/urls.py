from django.urls import path, include
from rest_framework import routers

from api.views import UpdateSetpoints
from aquarium.api.viewsets import PointValueViewSet, MeasuringDeviceViewSet, ExecutiveDeviceViewSet, \
    DeviceParameterMeasuredViewSet, SetpointViewSet
from aquarium.views import index, settings

app_name = 'aquarium'

router = routers.DefaultRouter()
router.register(r'point_value', PointValueViewSet, basename='point_value')
router.register(r'measuring_device', MeasuringDeviceViewSet, basename='measuring_device')
router.register(r'executive_device', ExecutiveDeviceViewSet, basename='executive_device')
router.register(r'device_parameter', DeviceParameterMeasuredViewSet, basename='device_parameter')
router.register(r'setpoint', SetpointViewSet, basename='setpoint')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/update_setpoints/', UpdateSetpoints.as_view()),
    path('', index, name='index'),
    path('settings/', settings, name='settings')

]