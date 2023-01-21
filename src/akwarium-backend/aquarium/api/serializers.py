from rest_framework import serializers

from aquarium.models import PointValue, MeasuringDevice, Parameter, ExecutiveDevice


class MeasuringDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasuringDevice
        fields = ['id', 'name']


class ExecutiveDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutiveDevice
        fields = ['id', 'name']


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['name', 'unit']


class PointValueSerializer(serializers.ModelSerializer):
    device = MeasuringDeviceSerializer()
    parameter = ParameterSerializer()

    class Meta:
        model = PointValue
        exclude = ['id']
