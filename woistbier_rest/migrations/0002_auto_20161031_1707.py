# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('woistbier_rest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='modified',
            field=models.DateTimeField(null=True, verbose_name='modified', auto_now=True),
        ),
        migrations.AddField(
            model_name='kiosk',
            name='modified',
            field=models.DateTimeField(null=True, verbose_name='modified', auto_now=True),
        ),
        migrations.AlterField(
            model_name='beerprice',
            name='modified',
            field=models.DateTimeField(null=True, verbose_name='modified', auto_now=True),
        ),
    ]
