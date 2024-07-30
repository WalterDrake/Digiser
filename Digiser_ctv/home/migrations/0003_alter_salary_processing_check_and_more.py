# Generated by Django 5.0.6 on 2024-07-30 13:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_rename_package_details_package_detail'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salary',
            name='processing_check',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='salary_processing_check', to='project.package'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='total_merging_votes',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='salary_total_merging_votes', to='project.package'),
        ),
        migrations.RemoveField(
            model_name='package_detail',
            name='package_name',
        ),
        migrations.AlterField(
            model_name='salary',
            name='total_erroring_fields',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='salary_total_erroring_fields', to='project.package'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='package_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.package'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='total_fields',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='salary_total_fields', to='project.package'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='total_votes',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='salary_total_votes', to='project.package'),
        ),
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
        migrations.AlterField(
            model_name='salary',
            name='project_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project'),
        ),
        migrations.DeleteModel(
            name='Package',
        ),
        migrations.DeleteModel(
            name='Package_detail',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]
