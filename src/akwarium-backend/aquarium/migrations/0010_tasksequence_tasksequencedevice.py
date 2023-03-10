# Generated by Django 4.1.5 on 2023-01-21 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aquarium', '0009_alter_executivedevice_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskSequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Nazwa sekwencji')),
            ],
            options={
                'verbose_name': 'Sekwencja układu',
                'verbose_name_plural': 'Sekwencje układów',
            },
        ),
        migrations.CreateModel(
            name='TaskSequenceDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(default=1, verbose_name='Kolejność wykonywania')),
                ('delay', models.PositiveSmallIntegerField(default=1000, verbose_name='Opóźnienie po wykonaniu')),
                ('output_value', models.BooleanField(default=True, verbose_name='Zadana wartość')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aquarium.executivedevice', verbose_name='Urządzenie wykonawcze')),
                ('sequence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aquarium.tasksequence', verbose_name='Sekwencja')),
            ],
            options={
                'verbose_name': 'Powiązanie urządzenia w sekwencji',
                'verbose_name_plural': 'Powiązania urządzeń w sekwencjach',
            },
        ),
    ]
