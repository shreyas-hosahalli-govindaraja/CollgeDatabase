# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-25 03:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crwdsource', '0015_auto_20170125_0323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='access_ticket',
            name='hash_key',
            field=models.CharField(default=b'91c0825da5556dc8c3d27728c0fa16', max_length=30, unique=True),
        ),
    ]
