# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class ConfiguracaoSistema(models.Model):
    # Configurações do SUAP
    url_suap = models.URLField(max_length=255, verbose_name='URL do SUAP')
    usuario_suap = models.CharField(max_length=255, verbose_name='Usuário do SUAP')
    senha_suap = models.CharField(max_length=255, verbose_name='Senha do SUAP')

    # Configurações do CKAN
    url_ckan = models.URLField(max_length=255, verbose_name='URL do CKAN')
    token_ckan = models.CharField(max_length=255, verbose_name='Token de Autenticação do CKAN')

    # Dados do Responsável pelo Portal de Dados Abertos
    nome_mantenedor = models.CharField(max_length=60, verbose_name='Nome do Mantenedor do Portal de Dados Abertos')
    email_mantenedor = models.EmailField(max_length=60, verbose_name='Email do Mantenedor do Portal de Dados Abertos')

    def __unicode__(self):
        return 'Configuração do Sistema #%s' % self.pk

    class Meta:
        verbose_name = 'Configuração do Sistema'
        verbose_name_plural = 'Configurações do Sistema'

class ConjuntoDeDados(models.Model):
    PERIDIOCIDADE_DIARIA = 1
    PERIDIOCIDADE_SEMANAL = 2
    PERIDIOCIDADE_MENSAL = 3
    PERIDIOCIDADE_SEMESTRAL = 4
    PERIDIOCIDADE_ANUAL = 5

    PERIODICIDADE_CHOICES = (
        (PERIDIOCIDADE_DIARIA, 'Diária'),
        (PERIDIOCIDADE_SEMANAL, 'Semanal'),
        (PERIDIOCIDADE_MENSAL, 'Mensal'),
        (PERIDIOCIDADE_SEMESTRAL, 'Semestral'),
        (PERIDIOCIDADE_ANUAL, 'Anual'),
    )

    # Configurações do Dataset no CKAN
    titulo = models.CharField(max_length=80, verbose_name='Título')
    descricao = models.TextField(verbose_name='Descrição')
    slug = models.SlugField(max_length=80, verbose_name='Slug')
    etiquetas = models.CharField(max_length=80, verbose_name='Etiquetas', help_text='Informe as etiquetas separadas por vírgula. Exemplo: "ensino, pesquisa, extensão"')

    # Configurações do Endpoint da API no SUAP
    url_endpoint = models.CharField(max_length=255, verbose_name='URL do Endpoint na API do SUAP')

    # Configurações da Extração
    periodicidade_extracao = models.PositiveIntegerField(choices=PERIODICIDADE_CHOICES, verbose_name='Periodicidade', default=PERIDIOCIDADE_SEMANAL)
    horario_extracao = models.TimeField(verbose_name='Horário de Execução da Extração', default='00:00')

    def __unicode__(self):
        return 'Conjunto de Dados: %s' % self.titulo

    class Meta:
        verbose_name = 'Conjunto de Dados'
        verbose_name_plural = 'Conjuntos de Dados'

class RegistroExtracao(models.Model):
    STATUS_FALHA = 1
    STATUS_SUCESSO = 2

    STATUS_CHOICES = (
        (STATUS_FALHA, 'Falha'),
        (STATUS_SUCESSO, 'Sucesso'),
    )

    conjunto_dados = models.ForeignKey('base.ConjuntoDeDados', verbose_name='Conjunto de Dados')
    data_horario_extracao = models.DateTimeField(verbose_name='Data e Horário da Extração', auto_now=True)
    quantidade_registros = models.PositiveIntegerField(verbose_name='Quantidade de Registros Extraídos')
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, verbose_name='Status')

    class Meta:
        verbose_name = 'Registro de Extração de Dados'
        verbose_name_plural = 'Registros de Extração de Dados'