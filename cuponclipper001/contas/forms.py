# -*- coding: utf-8 -*- 
from django import forms
from django.contrib.auth.forms import UserCreationForm
#from cuponclipper001.contas.models import UserProfile  
from django.core.mail import send_mail
import re
from django.contrib.auth.models import User
from cuponclipper001.contas import campo_personalizado
from django.contrib.auth import models
from django.contrib.auth.forms import UserCreationForm
from cuponclipper001.contas.models import MeuUser
from django.core.exceptions import MultipleObjectsReturned
from django.core.validators import EMPTY_VALUES
#from django.core.mail.message import BadHeaderError

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(),max_length=100)


class FormularioRegistro(forms.Form):
#class FormularioRegistro(UserCreationForm):        
    #user = forms.CharField(label=u'Usuario', max_length=30)
    nome = forms.CharField(label=u'Nome')
    sobrenome = forms.CharField(label=u'Sobrenome')
    email = forms.EmailField(label=u'Email')
    senha1 = forms.CharField(label=u'Senha',widget=forms.PasswordInput())
    senha2 = forms.CharField(label=u'Senha (Novamente)',widget=forms.PasswordInput())
    cpf = campo_personalizado.CPFField(label=u"Digite o seu CPF")
    telefone = campo_personalizado.TelefoneField(label=u"Digite o Telfone") 

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

