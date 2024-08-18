# Generated by Django 4.2.11 on 2024-08-18 10:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name='date')),
                ('title', models.CharField(blank=True, max_length=50, null=True, verbose_name='title')),
                ('message', models.TextField(blank=True, max_length=100, null=True, verbose_name='message')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name='date')),
                ('title', models.CharField(blank=True, max_length=50, null=True, verbose_name='title')),
                ('message', models.TextField(blank=True, max_length=100, null=True, verbose_name='message')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payroll_period', models.DateField(blank=True, null=True, verbose_name='payroll period')),
                ('type', models.CharField(blank=True, choices=[('Nhập', 'Nhập'), ('Check', 'Check')], max_length=10, null=True, verbose_name='type')),
                ('evaluation', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F')], max_length=1, null=True, verbose_name='evaluation')),
                ('basic_salary', models.IntegerField(blank=True, null=True, verbose_name='basic salary')),
                ('bonus_fine', models.IntegerField(blank=True, null=True, verbose_name='bonus/fine')),
                ('final_salary', models.IntegerField(blank=True, null=True, verbose_name='final salary')),
                ('note', models.CharField(blank=True, max_length=100, null=True, verbose_name='note')),
                ('package_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.package')),
                ('project_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
