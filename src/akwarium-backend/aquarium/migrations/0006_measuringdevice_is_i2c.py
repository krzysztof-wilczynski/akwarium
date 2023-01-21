# Generated by Django 4.1.5 on 2023-01-20 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aquarium', '0005_remove_measuringdevice_pin_measuringdevice_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='measuringdevice',
            name='is_i2c',
            field=models.BooleanField(default=False, verbose_name='I2C'),
        ),
    ]