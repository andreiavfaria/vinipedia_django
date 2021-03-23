# Generated by Django 3.1.7 on 2021-03-22 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0003_grape_grape_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='grape',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='producer',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='region',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='vintage',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='wine',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
