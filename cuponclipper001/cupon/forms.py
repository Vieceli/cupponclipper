# -*- coding: utf-8 -*-
'''
Created on 03/05/2011

@author: jhoni
'''

from django import forms
from django.forms import widgets
from datetime import date
import re
import pdb
from gmapi.forms.widgets import GoogleMap
#from massive002.engine import models as enginemodels

class MapForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width':410, 'height':410}))
    
class OfertaCheckoutForm(forms.Form):
    nome_completo           = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'size':'30'}) )
    senha            = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'size':'12'}) )
    senha_verifica     = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'size':'12'}))
    email               = forms.EmailField(help_text="voce@dominio.com", widget=forms.TextInput(attrs={'size':'30'}))
    quantidade = forms.ChoiceField(initial=1)
    
    def __init__(self, *args, **kwargs):
        self.lista = kwargs.pop('lista')   # recebe o valor da lista
        super(OfertaCheckoutForm, self).__init__(*args, **kwargs)

        self.fields['quantidade'].widget.choices = self.lista  # o conteudo da lista para a ser as opçoes de quantidade
        
    def clean(self):
        """
        Validate fields to make sure everything's as expected.
        - postalcode is in right format and actually exists
        - service actually exists
        """
        cd = self.cleaned_data

        if 'senha' in cd and 'senha_verifica' in cd:
            if self.cleaned_data['senha'] != self.cleaned_data['senha_verifica']:
                self._errors['senha'] = forms.util.ErrorList(["Senhas incompativeis!"])

        else:
            self._errors['senha'] = forms.util.ErrorList(["Confira sua senha"])

            raise forms.ValidationError('Por favor confirme sua senha')

        return cd
