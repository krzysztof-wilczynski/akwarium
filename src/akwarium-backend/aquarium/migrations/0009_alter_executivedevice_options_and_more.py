# Generated by Django 4.1.5 on 2023-01-21 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aquarium', '0008_pointvalue_parameter'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='executivedevice',
            options={'ordering': ('pin',), 'verbose_name': 'Urządzenie wykonawcze', 'verbose_name_plural': 'Urządzenia wykonawcze'},
        ),
        migrations.AlterModelOptions(
            name='measuringdevice',
            options={'ordering': ('address',), 'verbose_name': 'Urządzenie pomiarowe', 'verbose_name_plural': 'Urządzenia pomiarowe'},
        ),
        migrations.RemoveField(
            model_name='pointvalue',
            name='device',
        ),
        migrations.RemoveField(
            model_name='pointvalue',
            name='parameter',
        ),
        migrations.AddField(
            model_name='pointvalue',
            name='device_parameter',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='aquarium.deviceparametermeasured', verbose_name='Urządzenie i parametr'),
            preserve_default=False,
        ),
    ]
