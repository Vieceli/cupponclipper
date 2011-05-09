'''
Created on 29/04/2011

@author: jhoni
'''
from cuponclipper001.contas import campo_personalizado
from django.db import models


class BasePedidoInfo(models.Model):
    
    class Meta:
        abstract=True
        
    telefone = campo_personalizado.TelefoneField()
    cpf = campo_personalizado.CPFField()
    