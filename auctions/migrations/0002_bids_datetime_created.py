# Generated by Django 4.0.3 on 2022-04-01 10:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bids',
            name='datetime_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 1, 10, 49, 35, 309440, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
