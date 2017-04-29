# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from base.forms import ConfiguracaoSistemaForm
from base.models import ConfiguracaoSistema, ConjuntoDeDados


@admin.register(ConfiguracaoSistema)
class ConfiguracaoSistemaAdmin(admin.ModelAdmin):
    list_display = ('url_suap', 'url_ckan', 'nome_mantenedor', 'email_mantenedor')
    form = ConfiguracaoSistemaForm

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super(ConfiguracaoSistemaAdmin, self).has_add_permission(request)

@admin.register(ConjuntoDeDados)
class ConjuntoDeDadosAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'slug', 'periodicidade_extracao', 'horario_extracao')
    prepopulated_fields = {"slug": ("titulo",)}