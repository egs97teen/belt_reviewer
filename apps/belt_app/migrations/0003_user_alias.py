# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-24 05:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belt_app', '0002_auto_20170623_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='alias',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
