# Generated by Django 4.2.1 on 2023-07-31 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('admin', 'Admin'), ('profesor', 'Profesor')], max_length=10),
        ),
    ]