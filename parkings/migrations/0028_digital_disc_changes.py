# Generated by Django 2.2.3 on 2019-11-14 14:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkings', '0027_parkingcheck_performer'),
    ]

    operations = [
        migrations.AddField(
            model_name='parking',
            name='is_disc_parking',
            field=models.BooleanField(default=False, verbose_name='disc parking'),
        ),
        migrations.AlterField(
            model_name='parking',
            name='zone_id',
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(3)
                ],
                verbose_name='zone number'),
            ),
    ]
