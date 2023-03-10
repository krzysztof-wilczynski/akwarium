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
        ordering = ("address",)


class ExecutiveDevice(models.Model):
    name = models.CharField('Nazwa urządzenia', max_length=64, unique=True)
    pin = models.PositiveSmallIntegerField('Pin', unique=True)
    is_out = models.BooleanField('Wyjście', default=1)
    state = models.BooleanField('Stan', default=1)
    channel = models.FloatField('Kanał', null=True, blank=True)
    cron = models.BooleanField('Przełączanie przez cron', default=False)

    @admin.display(description="Kanał")
    def parsed_channel(self):
        return f"{self.channel:g}"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Urządzenie wykonawcze"
        verbose_name_plural = "Urządzenia wykonawcze"
        app_label = "aquarium"
        ordering = ("pin",)


class Setpoint(models.Model):
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name="Parametr")
    value = models.FloatField('Zadana wartość')

    def __str__(self):
        return f"{self.parameter.name} - {self.value}{self.parameter.unit}"

    class Meta:
        verbose_name = "Zadana wartość"
        verbose_name_plural = "Zadane wartości"
        app_label = "aquarium"


class TaskSequence(models.Model):
    name = models.CharField('Nazwa sekwencji', max_length=128)
    is_active = models.BooleanField('Czy aktywna', default=False)
    hysteresis = models.FloatField('Histereza', default=2)
    setpoint = models.ForeignKey(Setpoint, on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name="Powiązana wartość zadana")
    comparator = models.CharField("Komparator", max_length=4)
    startup_value = models.BooleanField('Stan przy uruchomieniu', default=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Sekwencja układu"
        verbose_name_plural = "Sekwencje układów"
        app_label = "aquarium"


class TaskPrecedingSequence(models.Model):
    sequence_to_check = models.ForeignKey(TaskSequence, on_delete=models.CASCADE, verbose_name="Sekwencja sprawdzana",
                                          related_name="task_sequence_checked")
    executed_sequence = models.ForeignKey(TaskSequence, on_delete=models.CASCADE, verbose_name="Sekwencja wykonywana",
                                          related_name="task_sequence_executed")

    def __str__(self):
        return f"Wykonaj {self.executed_sequence.name} jeśli {self.sequence_to_check.name} jest aktywna"

    class Meta:
        verbose_name = "Warunek wykonywania sekwencji"
        verbose_name_plural = "Warunki wykonywania sekwencji"
        app_label = "aquarium"


class TaskSequenceStep(models.Model):
    sequence = models.ForeignKey(TaskSequence, on_delete=models.CASCADE, verbose_name="Sekwencja")
    device = models.ForeignKey(ExecutiveDevice, on_delete=models.CASCADE, verbose_name="Urządzenie wykonawcze")
    order = models.PositiveSmallIntegerField("Kolejność wykonywania", default=1)
    delay = models.PositiveSmallIntegerField("Opóźnienie po wykonaniu", default=1000)
    output_value = models.BooleanField("Stan", default=True)

    def __str__(self):
        return f"{self.sequence} - {self.device.name}"

    class Meta:
        verbose_name = "Powiązanie urządzenia w sekwencji"
        verbose_name_plural = "Powiązania urządzeń w sekwencjach"
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


class PointValue(models.Model):
    device_parameter = models.ForeignKey(DeviceParameterMeasured, on_delete=models.CASCADE,
                                         verbose_name='Urządzenie i parametr')
    value = models.FloatField('Wartość pomiaru')
    timestamp = models.DateTimeField('Data pomiaru', auto_now_add=True)

    @admin.display(description="Wartość")
    def custom_value(self):
        return f"{self.value}{self.device_parameter.parameter.unit}"

    @admin.display(description="Urządzenie")
    def device_name(self):
        return self.device_parameter.device.name

    @admin.display(description="Parametr")
    def parameter_name(self):
        return self.device_parameter.parameter.name

    def __str__(self):
        return f"[{self.timestamp}] {self.device_parameter.device.name} - {self.value}"

    class Meta:
        verbose_name = "Pomiar"
        verbose_name_plural = "Pomiary"
        app_label = "aquarium"
