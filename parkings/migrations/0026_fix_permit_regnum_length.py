# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-13 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('parkings', '0025_parking_check'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permitlookupitem',
            name='registration_number',
            field=models.CharField(max_length=20)),
    ]
