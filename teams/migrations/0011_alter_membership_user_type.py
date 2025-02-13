# Generated by Django 5.1.5 on 2025-02-05 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0010_remove_team_owner_alter_membership_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='user_type',
            field=models.CharField(choices=[('Proprietário', 'Proprietário'), ('Administrador', 'Administrador'), ('Colaborador', 'Colaborador')], default='Colaborador', max_length=15),
        ),
    ]
