# Generated by Django 3.1.7 on 2021-09-16 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formapp', '0008_auto_20210916_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='address',
            field=models.CharField(default='tc03fl5li2', max_length=200),
        ),
    ]
