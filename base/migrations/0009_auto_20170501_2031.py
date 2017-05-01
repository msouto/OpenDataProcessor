# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-01 23:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_organizacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='conjuntodedados',
            name='organizacao',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Organizacao', verbose_name='Organiza\xe7\xe3o'),
        ),
        migrations.AddField(
            model_name='organizacao',
            name='id_ckan',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='ID no CKAN'),
        ),
    ]
