# Generated by Django 3.1.7 on 2021-09-19 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formapp', '0009_auto_20210916_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='address',
            field=models.CharField(default='8iupz1iepo', max_length=200),
        ),
    ]