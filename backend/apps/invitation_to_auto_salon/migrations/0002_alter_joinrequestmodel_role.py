# Generated by Django 5.2.1 on 2025-05-21 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invitation_to_auto_salon', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joinrequestmodel',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('seller', 'Seller'), ('mechanic', 'Mechanic')], default='pending', max_length=10),
        ),
    ]
