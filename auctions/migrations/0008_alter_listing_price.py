# Generated by Django 4.0.4 on 2022-04-29 12:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_listing_base_price_alter_listing_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
