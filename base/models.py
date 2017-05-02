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

class Organizacao(models.Model):
    nome = models.CharField(max_length=80, verbose_name='Nome', help_text='Exemplo: Instituto Federal do Rio Grande do Norte')
    descricao = models.TextField(verbose_name='Descrição', blank=True, null=True)
    slug = models.SlugField(max_length=80, verbose_name='Slug')
    url_logomarca = models.URLField(verbose_name='URL da Logomarca', blank=True, null=True)
    id_ckan = models.CharField(max_length=80, verbose_name='ID no CKAN', blank=True, null=True)

    def save(self, *args, **kwargs):
        from ckanapi import RemoteCKAN
        configuracao_sistema = ConfiguracaoSistema.objects.first()
        ckan = RemoteCKAN(configuracao_sistema.url_ckan, apikey=configuracao_sistema.token_ckan)

        try:
            if not self.id:
                # Criando a Organização no CKAN
                retorno = ckan.action.organization_create(
                    name=self.slug,
                    title=self.nome,
                    description=self.descricao,
                    image_url=self.url_logomarca
                )

                self.id_ckan = retorno.get('id')
            else:
                # Atualizando a Organização no CKAN
                retorno = ckan.action.organization_update(
                    id=self.id_ckan,
                    name=self.slug,
                    title=self.nome,
                    description=self.descricao,
                    image_url=self.url_logomarca
                )

                self.id_ckan = retorno.get('id')
        except:
            pass

        super(Organizacao, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = 'Organização'
        verbose_name_plural = 'Organizações'

class Grupo(models.Model):
    nome = models.CharField(max_length=80, verbose_name='Nome', help_text='Exemplo: Ensino')
    descricao = models.TextField(verbose_name='Descrição', blank=True, null=True)
    slug = models.SlugField(max_length=80, verbose_name='Slug')
    url_imagem = models.URLField(verbose_name='URL da Imagem', blank=True, null=True)
    id_ckan = models.CharField(max_length=80, verbose_name='ID no CKAN', blank=True, null=True)

    def save(self, *args, **kwargs):
        from ckanapi import RemoteCKAN
        configuracao_sistema = ConfiguracaoSistema.objects.first()
        ckan = RemoteCKAN(configuracao_sistema.url_ckan, apikey=configuracao_sistema.token_ckan)

        try:
            if not self.id:
                # Criando o Grupo no CKAN
                retorno = ckan.action.group_create(
                    name=self.slug,
                    title=self.nome,
                    description=self.descricao,
                    image_url=self.url_imagem
                )

                self.id_ckan = retorno.get('id')
            else:
                # Atualizando o Grupo no CKAN
                retorno = ckan.action.group_update(
                    id=self.id_ckan,
                    name=self.slug,
                    title=self.nome,
                    description=self.descricao,
                    image_url=self.url_imagem
                )

                self.id_ckan = retorno.get('id')
        except:
            pass

        super(Grupo, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'

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
    organizacao = models.ForeignKey('base.Organizacao', verbose_name='Organização', null=True)
    grupo = models.ForeignKey('base.Grupo', verbose_name='Grupo', null=True)
    titulo = models.CharField(max_length=80, verbose_name='Título')
    descricao = models.TextField(verbose_name='Descrição', blank=True, null=True)
    slug = models.SlugField(max_length=80, verbose_name='Slug')
    etiquetas = models.CharField(max_length=80, verbose_name='Etiquetas', help_text='Informe as etiquetas separadas por vírgula. Exemplo: "ensino, pesquisa, extensão"')
    id_ckan = models.CharField(max_length=80, verbose_name='ID no CKAN', blank=True, null=True)

    # Configurações do Endpoint da API no SUAP
    url_endpoint = models.CharField(max_length=255, verbose_name='URL do Endpoint na API do SUAP')

    # Configurações da Extração
    periodicidade_extracao = models.PositiveIntegerField(choices=PERIODICIDADE_CHOICES, verbose_name='Periodicidade', default=PERIDIOCIDADE_SEMANAL)
    horario_extracao = models.TimeField(verbose_name='Horário de Execução da Extração', default='00:00')

    def save(self, *args, **kwargs):
        from ckanapi import RemoteCKAN
        configuracao_sistema = ConfiguracaoSistema.objects.first()
        ckan = RemoteCKAN(configuracao_sistema.url_ckan, apikey=configuracao_sistema.token_ckan)

        try:
            if not self.id:
                # Criando o Conjunto de Dados no CKAN
                retorno = ckan.action.package_create(
                    name=self.slug,
                    title=self.titulo,
                    author='Sistema Unificado de Administração Pública (SUAP)', #TODO: Incluir campo na configuração
                    author_email='digti@ifrn.edu.br', #TODO: Incluir campo na configuração
                    maintainer=configuracao_sistema.nome_mantenedor,
                    maintainer_email=configuracao_sistema.email_mantenedor,
                    notes=self.descricao,
                    url=configuracao_sistema.url_suap + self.url_endpoint,
                    owner_org=self.organizacao.id_ckan
                )

                self.id_ckan = retorno.get('id')
            else:
                # Atualizando o Conjunto de Dados no CKAN
                retorno = ckan.action.package_update(
                    id=self.id_ckan,
                    name=self.slug,
                    title=self.titulo,
                    author='Sistema Unificado de Administração Pública (SUAP)',  # TODO: Incluir campo na configuração
                    author_email='digti@ifrn.edu.br',  # TODO: Incluir campo na configuração
                    maintainer=configuracao_sistema.nome_mantenedor,
                    maintainer_email=configuracao_sistema.email_mantenedor,
                    notes=self.descricao,
                    url=configuracao_sistema.url_suap + self.url_endpoint,
                    owner_org=self.organizacao.id_ckan
                )

                self.id_ckan = retorno.get('id')
        except:
            pass

        super(ConjuntoDeDados, self).save(*args, **kwargs)


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
    data_horario_inicio_extracao = models.DateTimeField(verbose_name='Data e Horário de Início da Extração')
    data_horario_termino_extracao = models.DateTimeField(verbose_name='Data e Horário de Término da Extração')
    quantidade_registros = models.PositiveIntegerField(verbose_name='Quantidade de Registros Extraídos')
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, verbose_name='Status')

    class Meta:
        verbose_name = 'Registro de Extração de Dados'
        verbose_name_plural = 'Registros de Extração de Dados'