# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-22 00:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudUnit', '0004_auto_20160521_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='duan',
            name='pureContent',
            field=models.TextField(null=True),
        ),
    ]
