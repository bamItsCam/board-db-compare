# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-03 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0004_auto_20170203_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbboards',
            name='adc',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='dbboards',
            name='gpio',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='dbboards',
            name='lan',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='dbboards',
            name='model_code',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='dbboards',
            name='usb_otg_port',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
