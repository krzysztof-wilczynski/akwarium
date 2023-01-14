from django.contrib import admin

from aquarium.models import MeasuringDevice, MeasurementType, HistoricalData


@admin.register(MeasurementType)
class MeasurementTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit']


@admin.register(MeasuringDevice)
class MeasuringDeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_type']


@admin.register(HistoricalData)
class HistoricalDataAdmin(admin.ModelAdmin):
    list_display = ['device', 'value', 'timestamp']
