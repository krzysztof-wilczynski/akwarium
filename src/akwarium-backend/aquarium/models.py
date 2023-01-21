from django.contrib import admin
from django.db import models


class Parameter(models.Model):
    name = models.CharField('Nazwa jednostki', max_length=32, unique=True)
    processed_name = models.CharField('Angielska nazwa', max_length=32, unique=True)
    unit = models.CharField('Jednostka', max_length=5)

    def __str__(self):
        return f"{self.name} - {self.unit}"

    class Meta:
        verbose_name = "Parametr"
        verbose_name_plural = "Parametry"
        app_label = "aquarium"


class MeasuringDevice(models.Model):
    name = models.CharField('Nazwa urządzenia', max_length=64, unique=True)
    address = models.CharField('Pin lub adres', max_length=4, unique=True)
    is_i2c = models.BooleanField("I2C", default=False)
    is_out = models.BooleanField('Wyjście', default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Urządzenie pomiarowe"
        verbose_name_plural = "Urządzenia pomiarowe"
        app_label = "aquarium"


class ExecutiveDevice(models.Model):
    name = models.CharField('Nazwa urządzenia', max_length=64, unique=True)
    pin = models.PositiveSmallIntegerField('Pin', unique=True)
    is_out = models.BooleanField('Wyjście', default=1)
    state = models.BooleanField('Stan', default=1)
    channel = models.FloatField('Kanał', null=True, blank=True)

    @admin.display(description="Kanał")
    def parsed_channel(self):
        return f"{self.channel:g}"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Urządzenie wykonawcze"
        verbose_name_plural = "Urządzenia wykonawcze"
        app_label = "aquarium"


class Setpoint(models.Model):
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name="Parametr")
    value = models.PositiveSmallIntegerField('Zadana wartość')

    def __str__(self):
        return f"{self.parameter.name} - {self.value}{self.parameter.unit}"

    class Meta:
        verbose_name = "Zadana wartość"
        verbose_name_plural = "Zadane wartości"
        app_label = "aquarium"


class PointValue(models.Model):
    device = models.ForeignKey(MeasuringDevice, on_delete=models.CASCADE, verbose_name='Urządzenie')
    value = models.FloatField('Wartość pomiaru')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name="Parametr")
    timestamp = models.DateTimeField('Data pomiaru', auto_now_add=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.device.name} - {self.value}"

    class Meta:
        verbose_name = "Pomiar"
        verbose_name_plural = "Pomiary"
        app_label = "aquarium"


class DeviceParameterMeasured(models.Model):
    device = models.ForeignKey(MeasuringDevice, on_delete=models.CASCADE, verbose_name='Urządzenie')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name='Parametr')

    def __str__(self):
        return f"{self.device} - {self.parameter.name}"

    class Meta:
        verbose_name = "Wartość zbierana przez urządzenie"
        verbose_name_plural = "Wartości zbierane przez urządzenia"
        app_label = "aquarium"
