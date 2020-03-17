# Generated by Django 3.0.4 on 2020-03-15 06:59

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee', '0010_auto_20200315_0851'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leavingtime',
            options={'ordering': ['date']},
        ),
        migrations.RemoveField(
            model_name='leavingtime',
            name='working_details',
        ),
        migrations.AddField(
            model_name='leavingtime',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='leavingtime',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
