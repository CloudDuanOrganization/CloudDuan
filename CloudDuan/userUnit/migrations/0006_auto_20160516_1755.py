# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-16 17:55
from __future__ import unicode_literals

from django.db import migrations, models
import userUnit.models


class Migration(migrations.Migration):

    dependencies = [
        ('userUnit', '0005_auto_20160516_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cduser',
            name='portrait',
            field=models.ImageField(default='User/defaultImage/1.jpg', upload_to=userUnit.models.userDirectoryPath),
        ),
    ]