# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-25 08:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontendapp', '0006_auto_20161023_0735'),
    ]

    operations = [
        migrations.AddField(
            model_name='college',
            name='model_pic',
            field=models.ImageField(default=b"{% static 'college_profile/not_available.png'%}", null=True, upload_to=b"{% static 'college_profile' %}"),
        ),
    ]
