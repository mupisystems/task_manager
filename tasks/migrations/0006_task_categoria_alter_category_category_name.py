# Generated by Django 5.1.5 on 2025-02-12 16:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_task_members_task_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
