# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import easy_thumbnails.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('brew', models.CharField(max_length=20, default='pils', choices=[('pils', 'Pils'), ('export', 'Export'), ('weizen', 'Weizen'), ('dunkel', 'Dunkel'), ('hell', 'Hell'), ('lager', 'Lager'), ('koelsch', 'Kölsch'), ('alt', 'Alt'), ('biermischgetraenk', 'Biermischgetränk'), ('starkbier', 'Starkbier'), ('stout', 'Stout')])),
                ('name', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BeerPrice',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('size', models.FloatField(max_length=1, default=0.5, choices=[(0.25, 'belgisch klein 0.25'), (0.33, 'klein 0.33'), (0.375, 'lambic 0.375'), (0.5, 'normal 0.5'), (0.6, 'italien normal 0.6'), (0.7, 'suedasien 0.7'), (0.8, 'australien groß 0.8'), (1.0, 'groß 1.0')])),
                ('price', models.IntegerField(validators=[django.core.validators.MaxValueValidator(400), django.core.validators.MinValueValidator(10)])),
                ('score', models.FloatField(default=1, max_length=1)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('beer', models.ForeignKey(to='woistbier_rest.Beer', related_name='related_beer', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(default='Anonymer Alkoholiker', max_length=25)),
                ('comment', models.CharField(max_length=400)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(blank=True, max_length=300, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Kiosk',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('street', models.CharField(verbose_name='street_name', max_length=150)),
                ('number', models.IntegerField(verbose_name='building_number')),
                ('zip_code', models.CharField(blank=True, null=True, max_length=6)),
                ('city', models.CharField(max_length=30)),
                ('name', models.CharField(blank=True, verbose_name='kiosk_name', max_length=160)),
                ('description', models.CharField(null=True, blank=True, verbose_name='description', max_length=600)),
                ('owner', models.CharField(null=True, blank=True, verbose_name='owners_name', max_length=100)),
                ('geo_lat', models.DecimalField(max_digits=13, decimal_places=10, blank=True, verbose_name='latitude', null=True)),
                ('geo_long', models.DecimalField(max_digits=13, decimal_places=10, blank=True, verbose_name='longitude', null=True)),
                ('is_valid_address', models.BooleanField(default=False, verbose_name='google_says_valid')),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='kiosk',
            unique_together=set([('city', 'street', 'number', 'zip_code')]),
        ),
        migrations.AddField(
            model_name='image',
            name='kiosk',
            field=models.ForeignKey(to='woistbier_rest.Kiosk', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='comment',
            name='kiosk',
            field=models.ForeignKey(to='woistbier_rest.Kiosk', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='beerprice',
            name='kiosk',
            field=models.ForeignKey(to='woistbier_rest.Kiosk', related_name='related_kiosk', on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='beerprice',
            unique_together=set([('beer', 'kiosk', 'size')]),
        ),
    ]
