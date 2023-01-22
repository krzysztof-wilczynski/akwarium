from django.contrib import admin

from aquarium.models import MeasuringDevice, Parameter, PointValue, ExecutiveDevice, Setpoint, DeviceParameterMeasured, \
    TaskSequence, TaskSequenceStep, TaskPrecedingSequence


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
    list_display = ['device_name', 'timestamp', 'parameter_name', 'custom_value']


@admin.register(Setpoint)
class SetPointAdmin(admin.ModelAdmin):
    list_display = ['parameter', 'value']


@admin.register(DeviceParameterMeasured)
class DeviceParameterMeasuredAdmin(admin.ModelAdmin):
    list_display = ['device', 'parameter']


@admin.register(TaskSequence)
class TaskSequenceAdmin(admin.ModelAdmin):
    list_display = ['name', 'hysteresis', 'is_active', 'setpoint']


@admin.register(TaskSequenceStep)
class TaskSequenceStepAdmin(admin.ModelAdmin):
    list_display = ['sequence', 'device', 'order', 'delay', 'output_value']


@admin.register(TaskPrecedingSequence)
class TaskPrecedingSequenceAdmin(admin.ModelAdmin):
    list_display = ["sequence_to_check", "executed_sequence"]