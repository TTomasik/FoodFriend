# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 15:23
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodfriend', '0005_auto_20170219_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quantity',
            name='quantity',
            field=models.DecimalField(blank=True, decimal_places=1, default=100, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
