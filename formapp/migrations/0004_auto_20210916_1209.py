# Generated by Django 3.1.7 on 2021-09-16 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formapp', '0003_auto_20210915_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='azmoon',
            name='Finished',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='class',
            name='address',
            field=models.CharField(default='46f1gubssi', max_length=200),
        ),
    ]
