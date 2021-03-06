# Generated by Django 3.1.7 on 2021-03-24 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0013_auto_20210324_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='wine',
            name='type',
            field=models.CharField(choices=[('white', 'White'), ('red', 'Red'), ('rosé', 'Rosé'), ('sparkling', 'Sparkling'), ('port', 'Port'), ('madeira', 'Madeira'), ('moscatel', 'Moscatel')], default='white', max_length=9),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='wine',
            unique_together={('name', 'producer', 'type')},
        ),
    ]
