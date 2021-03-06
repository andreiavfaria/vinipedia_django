# Generated by Django 3.1.7 on 2021-03-27 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0018_region_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='producer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='producer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='producers/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='producer',
            name='short_name',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='producer',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]
