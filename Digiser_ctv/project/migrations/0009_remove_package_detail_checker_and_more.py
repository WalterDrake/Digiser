# Generated by Django 4.2.11 on 2024-08-01 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_remove_package_detail_check_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package_detail',
            name='checker',
        ),
        migrations.RemoveField(
            model_name='package_detail',
            name='inserter',
        ),
        migrations.RemoveField(
            model_name='package_detail',
            name='sup_name',
        ),
    ]
