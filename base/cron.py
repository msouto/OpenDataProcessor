# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import kronos
from django.core.management import call_command

from base.models import ConjuntoDeDados


@kronos.register('* * * * *')
def executar_extracao_dados():
    now = datetime.datetime.now()
    ids_conjuntos_dados = ConjuntoDeDados.objects.filter(horario_extracao__hour=now.hour, horario_extracao__minute=now.minute).values_list('id', flat=True)

    if ids_conjuntos_dados:
        for id in ids_conjuntos_dados:
            call_command('extrair_dados', id)
    else:
        print 'Nenhum conjunto de dados a ser extraído no minuto.'