# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 15:23
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodfriend', '0006_auto_20170221_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quantity',
            name='quantity',
            field=models.FloatField(blank=True, default=100, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
