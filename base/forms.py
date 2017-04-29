# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from base.models import ConfiguracaoSistema


class ConfiguracaoSistemaForm(forms.ModelForm):
    senha_suap = forms.CharField(label='Senha do SUAP', max_length=50, min_length=0, widget=forms.PasswordInput)

    class Meta:
        model = ConfiguracaoSistema
        exclude = ('',)