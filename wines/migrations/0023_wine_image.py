# Generated by Django 3.1.7 on 2021-03-28 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0022_auto_20210327_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='wine',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='wines/%Y/%m/%d/'),
        ),
    ]
