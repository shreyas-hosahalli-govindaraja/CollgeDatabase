# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-20 17:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crwdsource', '0002_auto_20170120_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='access_ticket',
            name='hash_key',
            field=models.CharField(default=b'5bc5ebec0994b44d5b01da2964b34f', max_length=30, unique=True),
        ),
    ]
