# Generated by Django 5.2.1 on 2025-05-29 09:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto_salon_listings', '0002_alter_autosalonlistingmodel_last_view_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autosalonlistingmodel',
            name='city',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[A-z][a-z]{,29}$', 'Only alpha characters are allowed!')]),
        ),
        migrations.AlterField(
            model_name='autosalonlistingmodel',
            name='country',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[A-z][a-z]{,29}$', 'Only alpha characters are allowed!')]),
        ),
        migrations.AlterField(
            model_name='autosalonlistingmodel',
            name='region',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[A-z][a-z]{,29}$', 'Only alpha characters are allowed!')]),
        ),
    ]
