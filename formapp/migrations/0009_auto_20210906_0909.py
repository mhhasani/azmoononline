# Generated by Django 3.1.7 on 2021-09-06 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formapp', '0008_auto_20210906_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='azmoon',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='azmoon',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='address',
            field=models.CharField(default='xmm4i7g63j', max_length=200),
        ),
    ]
