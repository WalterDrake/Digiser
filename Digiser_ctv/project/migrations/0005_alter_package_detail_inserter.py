# Generated by Django 4.2.11 on 2024-08-01 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0004_alter_package_detail_checker_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package_detail',
            name='inserter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inserter', to=settings.AUTH_USER_MODEL),
        ),
    ]
