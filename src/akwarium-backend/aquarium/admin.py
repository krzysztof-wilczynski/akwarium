from django.contrib import admin

from aquarium.models import MeasuringDevice, Parameter, PointValue, ExecutiveDevice, Setpoint, DeviceParameterMeasured


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit']


@admin.register(MeasuringDevice)
class MeasuringDeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_out', 'is_i2c', 'address']


@admin.register(ExecutiveDevice)
class ExecutiveDeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'is_out', 'pin', 'parsed_channel']


@admin.register(PointValue)
class PointValueAdmin(admin.ModelAdmin):
    list_display = ['device', 'value', 'timestamp']


@admin.register(Setpoint)
class SetPointAdmin(admin.ModelAdmin):
    list_display = ['parameter', 'value']


@admin.register(DeviceParameterMeasured)
class DeviceParameterMeasuredAdmin(admin.ModelAdmin):
    list_display = ['device', 'parameter']
