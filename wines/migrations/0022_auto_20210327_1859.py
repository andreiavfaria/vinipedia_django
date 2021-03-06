# Generated by Django 3.1.7 on 2021-03-27 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0021_vintage_alcohol_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grape',
            name='origin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='grapes', to='wines.region'),
        ),
        migrations.AlterField(
            model_name='producer',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='local_producers', to='wines.region'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='wines', to='wines.producer'),
        ),
    ]
