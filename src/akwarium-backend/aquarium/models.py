from django.db import models


class MeasurementType(models.Model):
    name = models.CharField('Nazwa jednostki', max_length=32, unique=True)
    unit = models.CharField('Jednostka', max_length=5, unique=True)

    def __str__(self):
        return f"{self.name} - {self.unit}"

    class Meta:
        verbose_name = "Typ pomiaru"
        verbose_name_plural = "Typy pomiarów"
        app_label = "aquarium"


class MeasuringDevice(models.Model):
    name = models.CharField('Nazwa urządzenia', max_length=64, unique=True)
    # pin =
    measurement_type = models.ForeignKey(MeasurementType, on_delete=models.DO_NOTHING, verbose_name='Mierzone wartości')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Urządzenie pomiarowe"
        verbose_name_plural = "Urządzenia pomiarowe"
        app_label = "aquarium"


class HistoricalData(models.Model):
    device = models.ForeignKey(MeasuringDevice, on_delete=models.CASCADE, verbose_name='Urządzenie')
    value = models.FloatField('Wartość pomiaru')
    timestamp = models.DateTimeField('Data pomiaru', auto_now_add=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.device.name} - {self.value}{self.device.measurement_type.unit}"

    class Meta:
        verbose_name = "Pomiar historyczny"
        verbose_name_plural = "Pomiary historyczne"
        app_label = "aquarium"
