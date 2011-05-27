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
from cuponclipper001.contas import campo_personalizado
from cuponclipper001.contas.models import MeuUser
from django.core.exceptions import MultipleObjectsReturned
from django.core.mail import send_mail
from cuponclipper001.cupon.models import Cadastra_Email
#from massive002.engine import models as enginemodels

class MapForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width':410, 'height':410}))

class FormBuscar(forms.Form):
    query = forms.CharField(label=u'Procurar por: ',widget=forms.TextInput(attrs={'size': 32}))
    
class FormCadEmail(forms.Form):
    email = forms.EmailField(label=u'Digite o email: ',widget=forms.TextInput(attrs={'size': 32}))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Cadastra_Email.objects.get(email=email)
        except Cadastra_Email.DoesNotExist:
            return email
        raise forms.ValidationError('Email ja cadastrado')
    
class OfertaCheckoutForm(forms.Form):
    nome = forms.CharField(label=u'Nome')
    sobrenome = forms.CharField(label=u'Sobrenome')
    email = forms.EmailField(label=u'Email')
    senha1 = forms.CharField(label=u'Senha',widget=forms.PasswordInput())
    senha2 = forms.CharField(label=u'Senha (Novamente)',widget=forms.PasswordInput())
    cpf = campo_personalizado.CPFField(label=u"Digite o seu CPF")
    telefone = campo_personalizado.TelefoneField(label=u"Digite o Telfone")
    quantidade = forms.ChoiceField(initial=1) 
    
    def __init__(self, *args, **kwargs):
        self.lista = kwargs.pop('lista')   # recebe o valor da lista
        super(OfertaCheckoutForm, self).__init__(*args, **kwargs)
        self.fields['quantidade'].widget.choices = self.lista  # o conteudo da lista para a ser as opçoes de quantidade
        #self.fields['quantidade'].widget.CheckboxSelectMultiple = self.lista  # o conteudo da lista para a ser as opçoes de quantidade


    def clean_senha2(self):
        if 'senha1' in self.cleaned_data:
            senha1 = self.cleaned_data['senha1']
            senha2 = self.cleaned_data['senha2']
            if senha1 == senha2:
                return senha2
        raise forms.ValidationError('Senhas nao batem.')
  
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            MeuUser.objects.get(username=email)
        except MeuUser.DoesNotExist:
            return email
        raise forms.ValidationError('Usuario ja cadastrado')
      
    def clean_cpf(self):
        cpf_usuario = self.cleaned_data['cpf']
        print cpf_usuario
        try:
            MeuUser.objects.get(cpf=cpf_usuario)
        except MeuUser.DoesNotExist:
            return cpf_usuario
        except MultipleObjectsReturned:
            raise forms.ValidationError('CPF ja usado')

    def envia_email(self):
        #usuario = self.cleaned_data['username']
        senha = self.cleaned_data['senha1']
        email = self.cleaned_data['email']
        cpf = self.cleaned_data['cpf']
        titulo = u'Mensagem enviada pelo site na criacao do usuario'
        destino = 'veiodruida@gmail.com'
        texto = u"Bem vindo:" + email +"\nSua Senha: "+ senha + "\nSeu email: "+email + "\nSeu CPF" + cpf
        
        #texto nao esta correto quando chega na caixa de email
        if titulo and texto and destino:
            try:
                send_mail(
                    subject=titulo,
                    message=texto,
                    from_email=destino,#mudar destino posteriormente
                    recipient_list=[destino],
                    fail_silently=False
                    )
            except :
                print("Erro") 
  
  
    
   
        
#    def clean(self):
#        """
#        Validate fields to make sure everything's as expected.
#        - postalcode is in right format and actually exists
#        - service actually exists
#        """
#        cd = self.cleaned_data
#
#        if 'senha' in cd and 'senha_verifica' in cd:
#            if self.cleaned_data['senha'] != self.cleaned_data['senha_verifica']:
#                self._errors['senha'] = forms.util.ErrorList(["Senhas incompativeis!"])
#
#        else:
#            self._errors['senha'] = forms.util.ErrorList(["Confira sua senha"])
#
#            raise forms.ValidationError('Por favor confirme sua senha')
#
#        return cd
