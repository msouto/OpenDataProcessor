# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-29 19:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20170429_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracaosistema',
            name='url_ckan',
            field=models.URLField(max_length=255, verbose_name='URL do CKAN'),
        ),
        migrations.AlterField(
            model_name='conjuntodedados',
            name='url_endpoint',
            field=models.CharField(max_length=255, verbose_name='URL do Endpoint na API do SUAP'),
        ),
    ]
