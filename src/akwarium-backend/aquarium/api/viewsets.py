from rest_framework import viewsets

from aquarium.api.serializers import PointValueSerializer, MeasuringDeviceSerializer
from aquarium.models import PointValue, MeasuringDevice


class PointValueViewSet(viewsets.ModelViewSet):
    serializer_class = PointValueSerializer

    def get_queryset(self):
        # TODO: do przepisania, pobieranie najpierw wszystkiego jest w chuj nieefektywne
        device_id = self.request.query_params.get('device_id')
        parameter = self.request.query_params.get('parameter')

        queryset = PointValue.objects.all().order_by('timestamp')

        if device_id is not None:
            queryset.filter(device_id=device_id)
        if parameter is not None:
            queryset.filter(parameter__processed_name=parameter)

        return queryset


class MeasuringDeviceViewSet(viewsets.ModelViewSet):
    serializer_class = MeasuringDeviceSerializer

    def get_queryset(self):
        device_id = self.request.query_params.get('id')
        print(self.request.query_params)
        if device_id:
            queryset = MeasuringDevice.objects.filter(id=device_id)
            return queryset
        else:
            queryset = MeasuringDevice.objects.all()
            return queryset
