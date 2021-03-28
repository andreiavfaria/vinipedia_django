# Generated by Django 3.1.7 on 2021-03-22 19:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='Grape',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='Wine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='WineGrape',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grape', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grapes', to='wines.grape')),
                ('wine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wines', to='wines.wine')),
            ],
            options={
                'ordering': ('-wine', '-grape'),
                'unique_together': {('wine', 'grape')},
            },
        ),
        migrations.AddField(
            model_name='wine',
            name='grapes',
            field=models.ManyToManyField(through='wines.WineGrape', to='wines.Grape'),
        ),
        migrations.AddField(
            model_name='wine',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wines', to='wines.producer'),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='regions', to='wines.country')),
            ],
            options={
                'ordering': ('-name',),
                'unique_together': {('name', 'country')},
            },
        ),
        migrations.AddField(
            model_name='producer',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producers', to='wines.region'),
        ),
        migrations.AddField(
            model_name='grape',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grapes', to='wines.region'),
        ),
        migrations.AlterUniqueTogether(
            name='wine',
            unique_together={('name', 'producer')},
        ),
        migrations.CreateModel(
            name='Vintage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1700), django.core.validators.MaxValueValidator(2050)])),
                ('wine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vintages', to='wines.wine')),
            ],
            options={
                'ordering': ('-wine', '-year'),
                'unique_together': {('wine', 'year')},
            },
        ),
        migrations.CreateModel(
            name='GrapeAlias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('grape', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aliases', to='wines.grape')),
            ],
            options={
                'ordering': ('-name',),
                'unique_together': {('name', 'grape')},
            },
        ),
    ]