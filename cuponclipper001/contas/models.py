from django.db import models
from django.contrib.auth.models import User, UserManager
from cuponclipper001.checkout.BasePedidoInfo import BasePedidoInfo
from django.db.models.signals import post_save
from cuponclipper001.contas import campo_personalizado
from django.db.models import signals
#from ecomstore.checkout.models import BaseOrderInfo

#class MeuUser(models.Model):
class MeuUser(User):
    """ stores customer order information used with the last order placed; can be attached to the checkout order form
    as a convenience to registered customers who have placed an order in the past.
    
    """
    class Meta:
        verbose_name = u'Meu usuario'
        verbose_name_plural = u'Meus Usuarios'

        
    #user = models.ForeignKey(User)
    cpf = models.CharField(max_length=11)
    telefone = models.CharField(max_length=30)
    
    def __unicode__(self):
        return User.get_full_name(self)
    
    
    objects=UserManager()
