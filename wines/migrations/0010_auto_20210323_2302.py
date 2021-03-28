# Generated by Django 3.1.7 on 2021-03-23 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0009_auto_20210323_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winegrape',
            name='grape',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wines', to='wines.grape'),
        ),
        migrations.AlterField(
            model_name='winegrape',
            name='wine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grapes', to='wines.wine'),
        ),
    ]