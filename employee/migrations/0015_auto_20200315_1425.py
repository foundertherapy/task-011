# Generated by Django 3.0.4 on 2020-03-15 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0014_leavingtime_workingdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workingdetails',
            name='check_out',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
