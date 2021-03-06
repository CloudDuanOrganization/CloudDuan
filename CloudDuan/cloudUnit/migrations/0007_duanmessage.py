# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-23 18:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userUnit', '0006_auto_20160516_1755'),
        ('cloudUnit', '0006_duan_collector'),
    ]

    operations = [
        migrations.CreateModel(
            name='DuanMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=20)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('duan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='duanMessage', to='cloudUnit.Duan')),
                ('fromUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fromUser', to='userUnit.CdUser')),
                ('toUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='toUser', to='userUnit.CdUser')),
            ],
            options={
                'ordering': ['-time'],
            },
        ),
    ]
