# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-08 23:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('etrade', '0009_paper_paper_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderbuy',
            name='paper_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='etrade.Paper'),
        ),
    ]