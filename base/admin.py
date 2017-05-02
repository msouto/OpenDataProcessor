# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Group, User

from base.forms import ConfiguracaoSistemaForm
from base.models import ConfiguracaoSistema, ConjuntoDeDados, RegistroExtracao, Organizacao, Grupo

class OpenDataProcessorSite(AdminSite):
    site_header = 'OpenData Processor'
    index_title = 'Painel Administrativo'
    site_url = None
admin_site = OpenDataProcessorSite(name='OpenDataProcessorSite')

# Registrando os modelos da aplicação AUTH.
admin_site.register(Group)
admin_site.register(User)

# Registrando os modelos da aplicação BASE.
@admin.register(ConfiguracaoSistema, site=admin_site)
class ConfiguracaoSistemaAdmin(admin.ModelAdmin):
    list_display = ('url_suap', 'url_ckan', 'nome_mantenedor', 'email_mantenedor')
    form = ConfiguracaoSistemaForm
    fieldsets = (
        ('Configurações do SUAP', {
           'fields': ('url_suap', 'usuario_suap', 'senha_suap'),
        }),
        ('Configurações do CKAN', {
           'fields': ('url_ckan', 'token_ckan', 'nome_mantenedor', 'email_mantenedor')
        }),
    )

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super(ConfiguracaoSistemaAdmin, self).has_add_permission(request)

@admin.register(Organizacao, site=admin_site)
class OrganizacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'slug', 'id_ckan')
    exclude = ('id_ckan',)
    prepopulated_fields = {"slug": ("nome",)}

@admin.register(Grupo, site=admin_site)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'slug', 'id_ckan')
    exclude = ('id_ckan',)
    prepopulated_fields = {"slug": ("nome",)}

@admin.register(ConjuntoDeDados, site=admin_site)
class ConjuntoDeDadosAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'organizacao', 'grupo', 'descricao', 'slug', 'periodicidade_extracao', 'horario_extracao', 'id_ckan')
    exclude = ('id_ckan',)
    prepopulated_fields = {"slug": ("titulo",)}
    fieldsets = (
        ('Dados Gerais', {
            'fields': ('organizacao', 'grupo', 'titulo', 'descricao', 'slug', 'etiquetas')
        }),
        ('Endpoint', {
            'fields': ('url_endpoint',)
        }),
        ('Extração', {
            'fields': ('periodicidade_extracao', 'horario_extracao')
        }),
    )

@admin.register(RegistroExtracao, site=admin_site)
class RegistroExtracaoAdmin(admin.ModelAdmin):
    list_display = ('conjunto_dados', 'data_horario_inicio_extracao', 'data_horario_termino_extracao', 'quantidade_registros', 'status')
    fieldsets = (
        ('Conjunto de Dados', {
            'fields': ('conjunto_dados',),
        }),
        ('Resumo da Extração', {
            'fields': ('data_horario_inicio_extracao', 'data_horario_termino_extracao', 'quantidade_registros')
        }),
        ('Status', {
            'fields': ('status',),
        }),
    )