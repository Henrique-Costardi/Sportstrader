# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 20:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etrade', '0003_auto_20170303_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderexecuted',
            name='sport',
            field=models.CharField(default='', max_length=255),
        ),
    ]
