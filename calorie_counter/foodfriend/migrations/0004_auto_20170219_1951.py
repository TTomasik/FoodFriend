# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 19:51
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodfriend', '0003_auto_20170219_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextend',
            name='height',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(50)]),
        ),
        migrations.AlterField(
            model_name='userextend',
            name='weight',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]