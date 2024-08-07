# Generated by Django 4.2.11 on 2024-08-01 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_package_detail_check_status_package_detail_check_url_and_more'),
        ('home', '0003_salary_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='status',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.package_detail'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='type',
            field=models.CharField(blank=True, choices=[('I', 'Insert'), ('C', 'Check')], max_length=1, null=True, verbose_name='type'),
        ),
    ]
