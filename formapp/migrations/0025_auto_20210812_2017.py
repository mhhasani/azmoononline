# Generated by Django 3.1.7 on 2021-08-12 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formapp', '0024_auto_20210812_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='answer',
        ),
        migrations.AddField(
            model_name='question',
            name='answer1',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='answer2',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='answer3',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='answer4',
            field=models.CharField(max_length=200, null=True),
        ),
    ]