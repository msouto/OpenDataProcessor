# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracaosistema',
            name='email_mantenedor',
            field=models.EmailField(max_length=60, verbose_name='Email do Mantenedor do Portal de Dados Abertos'),
        ),
        migrations.AlterField(
            model_name='configuracaosistema',
            name='nome_mantenedor',
            field=models.CharField(max_length=60, verbose_name='Nome do Mantenedor do Portal de Dados Abertos'),
        ),
    ]
