# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-11 10:25
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20180310_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='文章内容'),
        ),
    ]
