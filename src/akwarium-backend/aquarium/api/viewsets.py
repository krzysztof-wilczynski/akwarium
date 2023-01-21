from rest_framework import viewsets

from aquarium.api.serializers import PointValueSerializer, MeasuringDeviceSerializer, ExecutiveDeviceSerializer, \
    DeviceParameterMeasuredSerializer
from aquarium.models import PointValue, MeasuringDevice, ExecutiveDevice, DeviceParameterMeasured


class PointValueViewSet(viewsets.ModelViewSet):
    serializer_class = PointValueSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id')
        if id:
            queryset = PointValue.objects.filter(device_parameter=id)
        else:
            queryset = PointValue.objects.all()

        return queryset.order_by('-timestamp')[:50][::-1]


class MeasuringDeviceViewSet(viewsets.ModelViewSet):
    serializer_class = MeasuringDeviceSerializer

    def get_queryset(self):
        device_id = self.request.query_params.get('id')
        if device_id:
            queryset = MeasuringDevice.objects.filter(id=device_id)
            return queryset
        else:
            queryset = MeasuringDevice.objects.all()
            return queryset


class ExecutiveDeviceViewSet(viewsets.ModelViewSet):
    serializer_class = ExecutiveDeviceSerializer

    def get_queryset(self):
        device_id = self.request.query_params.get('id')
        if device_id:
            queryset = ExecutiveDevice.objects.filter(id=device_id)
            return queryset
        else:
            return ExecutiveDevice.objects.all()


class DeviceParameterMeasuredViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceParameterMeasuredSerializer

    def get_queryset(self):
        metric_id = self.request.query_params.get('id')
        if metric_id:
            queryset = DeviceParameterMeasured.objects.filter(id=id)
            return queryset
        else:
            return DeviceParameterMeasured.objects.all()
