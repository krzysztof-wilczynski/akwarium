# Generated by Django 4.1.5 on 2023-01-22 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aquarium', '0019_tasksequence_comparator_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasksequence',
            name='hysteresis',
            field=models.FloatField(default=2, verbose_name='Histereza'),
        ),
    ]