# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from django.core.management.base import BaseCommand, CommandError
from base.models import ConfiguracaoSistema, ConjuntoDeDados, Organizacao, Grupo


class Command(BaseCommand):
    help = 'Consome os dados dos Conjuntos de Dados definidos no SUAP.'

    def handle(self, *args, **options):
        organizacoes = []
        grupos = []
        conjuntos_dados = []
        configuracao_sistema = ConfiguracaoSistema.objects.first()

        # Obtendo o Token de Autenticação
        params = {
            'username': configuracao_sistema.usuario_suap,
            'password': configuracao_sistema.senha_suap,
        }
        print '=> Obtendo o Token de Autenticação da API do SUAP'
        requisicao = requests.post(configuracao_sistema.url_suap + 'api/v2/autenticacao/token/', data=params)
        if requisicao.status_code == requests.codes.ok:
            token = requisicao.json().get('token')
            self.stdout.write(self.style.SUCCESS('=> Token: %s\n' % token))
        else:
            raise CommandError('Não foi possível obter o token de autenticação da API do SUAP.\nRetorno da API do SUAP: %s' % requisicao.json())

        # Obtendo as Organizações
        url = configuracao_sistema.url_suap + 'dados_abertos/api/organizacoes/'
        headers = {
            'Authorization': 'JWT %s' % token
        }
        try:
            while (True):
                print '=> Acessando a URL: %s' % url
                requisicao = requests.get(url, headers=headers)
                if requisicao.status_code == requests.codes.ok:
                    retorno_json = requisicao.json()
                    results = retorno_json.get('results')
                    organizacoes.extend(results)

                    if not retorno_json.get('next'):
                        break
                    else:
                        url = retorno_json.get('next')
                else:
                    raise CommandError('Não foi possível acessar a url %s.\nRetorno da API do SUAP: %s' % (url, requisicao.json()))
        except:
            raise CommandError('Não foi possível acessar a url %s.' % url)

        # Exibindo a quantidade de dados extraídos
        self.stdout.write(self.style.SUCCESS('=> %s organizações extraídas com sucesso.\n' % len(organizacoes)))


        # Obtendo os Grupos
        url = configuracao_sistema.url_suap + 'dados_abertos/api/grupos/'
        headers = {
            'Authorization': 'JWT %s' % token
        }
        try:
            while (True):
                print '=> Acessando a URL: %s' % url
                requisicao = requests.get(url, headers=headers)
                if requisicao.status_code == requests.codes.ok:
                    retorno_json = requisicao.json()
                    results = retorno_json.get('results')
                    grupos.extend(results)

                    if not retorno_json.get('next'):
                        break
                    else:
                        url = retorno_json.get('next')
                else:
                    raise CommandError('Não foi possível acessar a url %s.\nRetorno da API do SUAP: %s' % (url, requisicao.json()))
        except:
            raise CommandError('Não foi possível acessar a url %s.' % url)

        # Exibindo a quantidade de dados extraídos
        self.stdout.write(self.style.SUCCESS('=> %s grupos extraídas com sucesso.\n' % len(grupos)))

        # Obtendo os Conjuntos de Dados Abertos Cadastrados
        url = configuracao_sistema.url_suap + 'dados_abertos/api/conjuntos_dados_abertos/'
        headers = {
            'Authorization': 'JWT %s' % token
        }
        try:
            while (True):
                print '=> Acessando a URL: %s' % url
                requisicao = requests.get(url, headers=headers)
                if requisicao.status_code == requests.codes.ok:
                    retorno_json = requisicao.json()
                    results = retorno_json.get('results')
                    conjuntos_dados.extend(results)

                    if not retorno_json.get('next'):
                        break
                    else:
                        url = retorno_json.get('next')
                else:
                    raise CommandError('Não foi possível acessar a url %s.\nRetorno da API do SUAP: %s' % (url, requisicao.json()))
        except:
            raise CommandError('Não foi possível acessar a url %s.' % url)

        # Exibindo a quantidade de dados extraídos
        self.stdout.write(self.style.SUCCESS('=> %s conjuntos de dados extraídos com sucesso.\n' % len(conjuntos_dados)))

        # Cadastrando os Objetos coletados
        for item in organizacoes:
            organizacao, organizacao_criada = Organizacao.objects.update_or_create(
                nome=item.get('nome'),
                slug=item.get('slug'),
                descricao=item.get('descricao'),
                url_logomarca=item.get('url_logomarca')
            )

        for item in grupos:
            grupo, grupo_criado = Grupo.objects.update_or_create(
                nome=item.get('nome'),
                slug=item.get('slug'),
                descricao=item.get('descricao'),
                url_imagem=item.get('url_imagem')
            )

        for item in conjuntos_dados:
            conjunto = ConjuntoDeDados.objects.update_or_create(
                titulo=item.get('titulo'),
                slug=item.get('slug'),
                descricao=item.get('descricao'),
                etiquetas=', '.join(item.get('etiquetas')),
                url_endpoint=item.get('url'),
                periodicidade_extracao=dict(ConjuntoDeDados.PERIODICIDADE_CHOICES).values().index(item.get('periodicidade_extracao')),
                horario_extracao=item.get('horario_extracao'),
                organizacao=Organizacao.objects.get(slug=item.get('organizacao').get('slug')),
                grupo=Grupo.objects.get(slug=item.get('grupo').get('slug')),
            )