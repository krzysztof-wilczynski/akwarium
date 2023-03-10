from rest_framework import serializers

from aquarium.models import PointValue, MeasuringDevice, Parameter, ExecutiveDevice, DeviceParameterMeasured, Setpoint


class MeasuringDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasuringDevice
        fields = ['id', 'name']


class DeviceParameterMeasuredSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceParameterMeasured
        fields = '__all__'
        depth = 1


class ExecutiveDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutiveDevice
        fields = ['id', 'name']


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['name', 'unit']


class PointValueSerializer(serializers.ModelSerializer):
    # device = MeasuringDeviceSerializer()
    # parameter = ParameterSerializer()

    class Meta:
        model = PointValue
        fields = '__all__'


class SetpointSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()

    class Meta:
        model = Setpoint
        fields = '__all__'
