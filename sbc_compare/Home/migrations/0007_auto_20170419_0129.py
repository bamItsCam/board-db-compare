# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-19 01:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0006_dbboards_board_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='dbSelectedBoards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boardName', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='dbboards',
            name='board_name',
        ),
        migrations.RemoveField(
            model_name='dbboards',
            name='usb_otg',
        ),
    ]
