# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-02 13:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_grupo'),
    ]

    operations = [
        migrations.AddField(
            model_name='conjuntodedados',
            name='grupo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Grupo', verbose_name='Grupo'),
        ),
    ]
