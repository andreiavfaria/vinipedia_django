# Generated by Django 3.1.7 on 2021-03-27 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0017_country_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='regions/%Y/%m/%d/'),
        ),
    ]
