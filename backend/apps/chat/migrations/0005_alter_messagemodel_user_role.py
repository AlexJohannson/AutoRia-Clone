# Generated by Django 5.2.1 on 2025-06-01 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_messagemodel_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagemodel',
            name='user_role',
            field=models.TextField(),
        ),
    ]
