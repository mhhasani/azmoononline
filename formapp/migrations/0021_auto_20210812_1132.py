# Generated by Django 3.1.7 on 2021-08-12 07:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('formapp', '0020_auto_20210812_1118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='password',
        ),
        migrations.AddField(
            model_name='participant',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]