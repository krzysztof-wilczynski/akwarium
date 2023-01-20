from django.contrib import admin

from aquarium.models import MeasuringDevice, MeasurementType, HistoricalData, ExecutiveDevice


@admin.register(MeasurementType)
class MeasurementTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit']


@admin.register(MeasuringDevice)
class MeasuringDeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_type', 'is_out', 'pin']


@admin.register(ExecutiveDevice)
class ExecutiveDeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'is_out', 'pin', 'parsed_channel']


@admin.register(HistoricalData)
class HistoricalDataAdmin(admin.ModelAdmin):
    list_display = ['device', 'value', 'timestamp']
