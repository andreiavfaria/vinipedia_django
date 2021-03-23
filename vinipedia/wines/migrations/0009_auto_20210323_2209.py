# Generated by Django 3.1.7 on 2021-03-23 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0008_auto_20210323_2147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grape',
            old_name='grape_type',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='wine',
            old_name='grapes',
            new_name='grape_varieties',
        ),
        migrations.AlterField(
            model_name='producerregion',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='regions', to='wines.producer'),
        ),
        migrations.AlterField(
            model_name='producerregion',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producers', to='wines.region'),
        ),
    ]
