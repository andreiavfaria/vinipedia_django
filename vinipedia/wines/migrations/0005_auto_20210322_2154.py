# Generated by Django 3.1.7 on 2021-03-22 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0004_auto_20210322_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grape',
            name='origin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grapes', to='wines.region'),
        ),
    ]
