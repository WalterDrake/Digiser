# Generated by Django 5.0.6 on 2024-07-01 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_customuser_birthday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='birthday',
        ),
    ]
