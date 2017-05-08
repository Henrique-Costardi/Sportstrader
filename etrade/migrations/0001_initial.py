# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 20:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderBuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=255, unique=True)),
                ('owner_id', models.CharField(max_length=255)),
                ('owner_dna', models.CharField(max_length=255)),
                ('paper_name', models.CharField(max_length=255)),
                ('paper_code', models.CharField(default='', max_length=255)),
                ('order_value', models.FloatField(default=1.0)),
                ('order_qty', models.IntegerField(default=10000)),
                ('status', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OrderExecuted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(default='', max_length=255, unique=True)),
                ('buyer_id', models.CharField(max_length=255)),
                ('buyer_dna', models.CharField(max_length=255)),
                ('seller_id', models.CharField(max_length=255)),
                ('seller_dna', models.CharField(max_length=255)),
                ('paper_name', models.CharField(max_length=255)),
                ('paper_code', models.CharField(default='', max_length=255)),
                ('order_value', models.FloatField(default=1.0)),
                ('executed_qty', models.IntegerField(default=10000)),
                ('buy_id', models.CharField(default='', max_length=255)),
                ('sell_id', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OrderSell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=255, unique=True)),
                ('owner_id', models.CharField(default='', max_length=255)),
                ('owner_dna', models.CharField(max_length=255)),
                ('paper_name', models.CharField(max_length=255)),
                ('paper_code', models.CharField(default='', max_length=255)),
                ('order_value', models.FloatField(default=1.0)),
                ('order_qty', models.IntegerField(default=10000)),
                ('status', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper_code', models.CharField(max_length=255, unique=True)),
                ('paper_name', models.CharField(max_length=255, unique=True)),
                ('paper_value', models.FloatField(default=1.0)),
                ('paper_initial_qty', models.IntegerField(default=10000)),
                ('paper_current_qty', models.IntegerField(default=10000)),
                ('paper_highest_value', models.FloatField(default=1.0)),
                ('paper_lowest_value', models.FloatField(default=1.0)),
                ('sport', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PaperBank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_id', models.CharField(default='', max_length=255)),
                ('owner_dna', models.CharField(max_length=255)),
                ('paper_name', models.CharField(default='', max_length=255)),
                ('paper_value', models.CharField(default=1.0, max_length=255)),
                ('paper_qty', models.IntegerField(default=10000)),
                ('sport', models.CharField(default='', max_length=255)),
            ],
        ),
    ]
