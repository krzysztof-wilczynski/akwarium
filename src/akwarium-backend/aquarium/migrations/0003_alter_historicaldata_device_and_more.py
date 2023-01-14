# Generated by Django 4.1.5 on 2023-01-14 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aquarium', '0002_alter_historicaldata_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaldata',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aquarium.measuringdevice', verbose_name='Urządzenie'),
        ),
        migrations.AlterField(
            model_name='historicaldata',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data pomiaru'),
        ),
        migrations.AlterField(
            model_name='historicaldata',
            name='value',
            field=models.FloatField(verbose_name='Wartość pomiaru'),
        ),
        migrations.AlterField(
            model_name='measurementtype',
            name='name',
            field=models.CharField(max_length=32, unique=True, verbose_name='Nazwa jednostki'),
        ),
        migrations.AlterField(
            model_name='measurementtype',
            name='unit',
            field=models.CharField(max_length=5, unique=True, verbose_name='Jednostka'),
        ),
        migrations.AlterField(
            model_name='measuringdevice',
            name='measurement_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='aquarium.measurementtype', verbose_name='Mierzone wartości'),
        ),
        migrations.AlterField(
            model_name='measuringdevice',
            name='name',
            field=models.CharField(max_length=64, unique=True, verbose_name='Nazwa urządzenia'),
        ),
    ]