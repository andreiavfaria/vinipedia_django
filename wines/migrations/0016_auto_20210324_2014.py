# Generated by Django 3.1.7 on 2021-03-24 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0015_auto_20210324_1915'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('wine', 'vintage', 'user'), name='wine_vintage_user_constraint'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(condition=models.Q(vintage=None), fields=('wine', 'user'), name='wine_user_vintagenull_constraint'),
        ),
    ]