# Generated by Django 3.1.7 on 2021-03-22 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0002_auto_20210322_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='grape',
            name='grape_type',
            field=models.CharField(choices=[('white', 'White'), ('red', 'Red')], default=1, max_length=5),
            preserve_default=False,
        ),
    ]
