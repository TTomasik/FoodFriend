# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 19:40
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodfriend', '0002_auto_20170216_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextend',
            name='age',
            field=models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(150), django.core.validators.MinValueValidator(1)]),
        ),
    ]
