# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
from types import StringTypes

import requests
import unicodecsv as csv
from ckanapi.remoteckan import RemoteCKAN
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError

from base.models import ConfiguracaoSistema, ConjuntoDeDados, RegistroExtracao

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
                chave_cache = 'dados_extraidos_%s' % conjunto_dados.slug
            except ConjuntoDeDados.DoesNotExist:
                raise CommandError('O Conjunto de Dados "%s" não existe.' % conjunto_dados_id)
            except ConfiguracaoSistema.DoesNotExist:
                raise CommandError('É necessário definir as Configurações do Sistema.')

            if not cache.get(chave_cache):
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
                            retorno_json = requisicao.json()
                            results = retorno_json.get('results')
                            dados.extend(results)
                            self.stdout.write(self.style.SUCCESS('=> %s dados extraídos.' % len(results)))

                            if not retorno_json.get('next'):
                                break
                            else:
                                url = retorno_json.get('next')
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
                cache.set(chave_cache, dados)
                self.stdout.write(self.style.SUCCESS('=> Os dados extraídos foram inseridos no cache através da chave "%s".' % chave_cache))
            else:
                self.stdout.write(self.style.SUCCESS('=> Os dados extraídos foram lidos do cache através da chave "%s".' % chave_cache))
                dados = cache.get(chave_cache)

            # Salvando o arquivo JSON para carregar no CKAN.
            filename_json = '/tmp/dados_extraidos_%s.json' % conjunto_dados.slug
            with open(filename_json, 'w') as arquivo_json:
                json.dump(dados, arquivo_json)

            # Salvando o arquivo CSV para carregar no CKAN.
            filename_csv = '/tmp/dados_extraidos_%s.csv' % conjunto_dados.slug
            with open(filename_csv, 'wb') as csv_file:
                write_header = True
                item_keys = []
                writer = csv.writer(csv_file, delimiter=str(";"), quotechar=str('"'))

                for item in dados:
                    item_values = []
                    for key in item:
                        if write_header:
                            item_keys.append(key)

                        value = item.get(key, '')
                        if isinstance(value, StringTypes):
                            item_values.append(value.encode('utf-8'))
                        elif isinstance(value, list) or isinstance(value, tuple):
                            item_values.append(', '.join(value))
                        else:
                            item_values.append(value)

                    if write_header:
                        writer.writerow(item_keys)
                        write_header = False

                    writer.writerow(item_values)

            # Enviando o arquivo CSV para o CKAN
            ckan = RemoteCKAN(configuracao_sistema.url_ckan, apikey=configuracao_sistema.token_ckan)
            retorno_json = ckan.action.package_show(id=conjunto_dados.id_ckan)

            if retorno_json.get('num_resources') == 0:
                for filename in [filename_json, filename_csv]:
                    ckan.action.resource_create(
                        package_id=conjunto_dados.id_ckan,
                        name=conjunto_dados.titulo,
                        url=conjunto_dados.slug,
                        upload=open(filename, 'rb')
                    )
            else:
                for index, filename in enumerate([filename_json, filename_csv]):
                    id_recurso = retorno_json.get('resources')[index].get('id')
                    ckan.action.resource_update(
                        id=id_recurso,
                        name=conjunto_dados.titulo,
                        url=conjunto_dados.slug,
                        upload=open(filename, 'rb')
                    )

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