# Generated by Django 5.2 on 2025-05-09 14:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_model', '0001_initial'),
        ('listings', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listingsellersmodel',
            name='model',
        ),
        migrations.AddField(
            model_name='listingsellersmodel',
            name='model_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='car_model.carmodelmodel'),
            preserve_default=False,
        ),
    ]
