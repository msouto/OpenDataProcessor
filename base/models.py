# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class ConfiguracaoSistema(models.Model):
    # Configurações do SUAP
    url_suap = models.URLField(max_length=255, verbose_name='URL da API do SUAP')
    usuario_suap = models.CharField(max_length=255, verbose_name='Usuário do SUAP')
    senha_suap = models.CharField(max_length=255, verbose_name='Senha do SUAP')

    # Configurações do CKAN
    url_ckan = models.URLField(max_length=255, verbose_name='URL da API do CKAN')
    token_ckan = models.CharField(max_length=255, verbose_name='Token de Autenticação do CKAN')

    # Dados do Responsável pelo Portal de Dados Abertos
    nome_mantenedor = models.CharField(max_length=60, verbose_name='Nome do Mantenedor do Portal de Dados Abertos')
    email_mantenedor = models.EmailField(max_length=60, verbose_name='Email do Mantenedor do Portal de Dados Abertos')

    class Meta:
        verbose_name = 'Configuração do Sistema'
        verbose_name_plural = 'Configurações do Sistema'