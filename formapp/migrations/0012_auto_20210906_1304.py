# Generated by Django 3.1.7 on 2021-09-06 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formapp', '0011_auto_20210906_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='address',
            field=models.CharField(default='2pwbnb0p3d', max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='Q_image',
            field=models.ImageField(blank=True, default='8.jpeg', upload_to='questions_image'),
        ),
    ]
