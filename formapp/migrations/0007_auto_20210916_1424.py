# Generated by Django 3.1.7 on 2021-09-16 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formapp', '0006_auto_20210916_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='address',
            field=models.CharField(default='lq5ywdtrle', max_length=200),
        ),
    ]
