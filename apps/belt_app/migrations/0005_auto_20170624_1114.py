# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-24 18:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('belt_app', '0004_book_favorites'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='book_written',
            new_name='books_written',
        ),
    ]