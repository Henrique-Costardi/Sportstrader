# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-08 22:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etrade', '0007_paper_last_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='paper_reference_value',
            field=models.FloatField(default=1.0),
        ),
    ]
