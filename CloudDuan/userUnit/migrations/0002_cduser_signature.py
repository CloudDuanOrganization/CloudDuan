# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-03 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userUnit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cduser',
            name='signature',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
