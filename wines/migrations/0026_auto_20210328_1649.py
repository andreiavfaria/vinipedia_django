# Generated by Django 3.1.7 on 2021-03-28 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0025_auto_20210328_1627'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='wine',
            name='name_type_producer_constraint',
        ),
        migrations.AlterUniqueTogether(
            name='wine',
            unique_together={('name', 'type', 'producer')},
        ),
    ]
