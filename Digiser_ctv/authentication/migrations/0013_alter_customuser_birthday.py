# Generated by Django 5.0.6 on 2024-07-01 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_alter_customuser_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birthday',
            field=models.CharField(blank=True, max_length=10, verbose_name='birthday'),
        ),
    ]
