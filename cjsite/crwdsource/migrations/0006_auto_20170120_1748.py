# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-20 17:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crwdsource', '0005_auto_20170120_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='access_ticket',
            name='hash_key',
            field=models.CharField(default=b'2b75826ece5fe7ed180e107f727438', max_length=30, unique=True),
        ),
    ]
