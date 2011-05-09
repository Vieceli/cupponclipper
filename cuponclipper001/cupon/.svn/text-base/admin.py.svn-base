# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Anunciante,Localizacao,Cupon,Categoria,Cupon_Adquirido
from django.contrib.auth.models import User
from cuponclipper001.contas.models import MeuUser

from django.contrib.auth.admin import UserAdmin

class AnuncianteAdmin(admin.ModelAdmin):
    """admin class"""

class CategoriaAdmin(admin.ModelAdmin):
    """admin class"""
    prepopulated_fields = {
        'slug': ( 'nome', )
    }

class CuponAdquiridoAdmin(admin.ModelAdmin):
    """admin class"""
    list_display = ['usuario', 'cupon', 'status']
    list_filter = ('usuario', 'cupon')
    list_per_page = 100
    search_fields = ['usuario', 'cupon']
    
class CuponAdmin(admin.ModelAdmin):
    """admin class"""
    list_display = ['titulo', 'anunciante', 'ativo',]
    list_filter = ('titulo', 'anunciante','ativo')
    list_per_page = 100
    search_fields = ['titulo', 'anunciante','ativo'] 
    prepopulated_fields = {
        'slug': ( 'titulo', ),
    }


class LocalizacaoAdmin(admin.ModelAdmin):
    """admin class"""
    list_display = ['cidade', 'estado', 'ativo']
    list_per_page = 100
    search_fields = ['cidade']
    prepopulated_fields = {
        'slug': ( 'cidade', )
    }

admin.site.unregister(User)

class CustomUserAdmin(admin.ModelAdmin):
    """ka"""
    #list_display = ['email','first_name', 'last_name', 'cpf', 'telefone']
    


admin.site.register(MeuUser, CustomUserAdmin)


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Cupon, CuponAdmin)
admin.site.register(Cupon_Adquirido, CuponAdquiridoAdmin)
admin.site.register(Anunciante, AnuncianteAdmin)
admin.site.register(Localizacao, LocalizacaoAdmin)
