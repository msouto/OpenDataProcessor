# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from base.models import ConfiguracaoSistema, ConjuntoDeDados, RegistroExtracao
import requests
import datetime

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('conjunto_dados_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for conjunto_dados_id in options['conjunto_dados_id']:
            data_inicio_extracao = datetime.datetime.now()
            self.stdout.write(self.style.SUCCESS('== Iniciando a extração do Conjunto de Dados #%s ==\n' % conjunto_dados_id))
            dados = []

            try:
                token = None
                conjunto_dados = ConjuntoDeDados.objects.get(pk=conjunto_dados_id)
                configuracao_sistema = ConfiguracaoSistema.objects.first()
            except ConjuntoDeDados.DoesNotExist:
                raise CommandError('O Conjunto de Dados "%s" não existe.' % conjunto_dados_id)
            except ConfiguracaoSistema.DoesNotExist:
                raise CommandError('É necessário definir as Configurações do Sistema.')

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

            # Executando a extração dos dados da API do SUAP.
            url = configuracao_sistema.url_suap + conjunto_dados.url_endpoint
            headers = {
                'Authorization':'JWT %s' % token
            }

            try:
                while(True):
                    print '=> Acessando a URL: %s' % url
                    requisicao = requests.get(url, headers=headers)
                    if requisicao.status_code == requests.codes.ok:
                        json = requisicao.json()
                        results = json.get('results')
                        dados.extend(results)
                        self.stdout.write(self.style.SUCCESS('=> %s dados extraídos.' % len(results)))

                        if not json.get('next'):
                            break
                        else:
                            url = json.get('next')
                    else:
                        raise CommandError('Não foi possível acessar o endpoint do conjunto de dados.\nRetorno da API do SUAP: %s' % requisicao.json())
            except:
                RegistroExtracao.objects.create(
                    conjunto_dados=conjunto_dados,
                    data_horario_inicio_extracao=data_inicio_extracao,
                    data_horario_termino_extracao=datetime.datetime.now(),
                    quantidade_registros=0,
                    status=RegistroExtracao.STATUS_FALHA
                )
                raise CommandError('Não foi possível acessar o endpoint do conjunto de dados.')


            # Exibindo a quantidade de dados extraídos
            self.stdout.write(self.style.SUCCESS('\n=> %s dados extraídos com sucesso.' % len(dados)))

            # Fazendo cache dos dados extraídos
            chave_cache = 'dados_extraidos_%s' % conjunto_dados.slug
            cache.set(chave_cache, dados)
            self.stdout.write(self.style.SUCCESS('=> Os dados extraídos foram inseridos no cache através da chave "%s".' % chave_cache))

            # Salvando o Registro de Execução da Extração.
            RegistroExtracao.objects.create(
                conjunto_dados=conjunto_dados,
                data_horario_inicio_extracao=data_inicio_extracao,
                data_horario_termino_extracao=datetime.datetime.now(),
                quantidade_registros=len(dados),
                status=RegistroExtracao.STATUS_SUCESSO
            )

            # Exibindo a mensagem de Sucesso na Extração.
            self.stdout.write(self.style.SUCCESS('\n== Finalizando a extração do conjunto de dados #%s ==\n' % conjunto_dados_id))