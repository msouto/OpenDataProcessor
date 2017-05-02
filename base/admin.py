# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from base.forms import ConfiguracaoSistemaForm
from base.models import ConfiguracaoSistema, ConjuntoDeDados, RegistroExtracao, Organizacao, Grupo


@admin.register(ConfiguracaoSistema)
class ConfiguracaoSistemaAdmin(admin.ModelAdmin):
    list_display = ('url_suap', 'url_ckan', 'nome_mantenedor', 'email_mantenedor')
    form = ConfiguracaoSistemaForm

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super(ConfiguracaoSistemaAdmin, self).has_add_permission(request)

@admin.register(Organizacao)
class OrganizacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'slug', 'id_ckan')
    exclude = ('id_ckan',)
    prepopulated_fields = {"slug": ("nome",)}

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'slug', 'id_ckan')
    exclude = ('id_ckan',)
    prepopulated_fields = {"slug": ("nome",)}

@admin.register(ConjuntoDeDados)
class ConjuntoDeDadosAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'organizacao', 'descricao', 'slug', 'periodicidade_extracao', 'horario_extracao', 'id_ckan')
    exclude = ('id_ckan',)
    prepopulated_fields = {"slug": ("titulo",)}

@admin.register(RegistroExtracao)
class RegistroExtracaoAdmin(admin.ModelAdmin):
    list_display = ('conjunto_dados', 'data_horario_inicio_extracao', 'data_horario_termino_extracao', 'quantidade_registros', 'status')