# Generated by Django 4.1.5 on 2023-01-21 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aquarium', '0013_alter_setpoint_is_max_alter_setpoint_sequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasksequence',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Czy aktywna'),
        ),
        migrations.CreateModel(
            name='TaskPrecedingSequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_sequence_executed', to='aquarium.tasksequence', verbose_name='Sekwencja wykonywana')),
                ('sequence_to_check', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_sequence_checked', to='aquarium.tasksequence', verbose_name='Sekwencja sprawdzana')),
            ],
            options={
                'verbose_name': 'Warunek wykonywania sekwencji',
                'verbose_name_plural': 'Warunki wykonywania sekwencji',
            },
        ),
    ]
