# Generated by Django 4.0.3 on 2022-04-05 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_rename_listings_watchlist_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]
