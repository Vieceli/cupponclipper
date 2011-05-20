# -*- coding: utf-8 -*- 
from django.db import models
from django.core.urlresolvers import reverse
import datetime
import time
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
#from tagging.models import TagField


OFERTA_IMG = 'cupon_imagens/'
OFERTA_MINI = 'cupon_mini/'

STATUS_EM_ESPERA = 1
STATUS_USADO = 2
STATUS_CANCELADO = 3

STATUS = (
  (STATUS_EM_ESPERA, "Adquirido - Em Espera"),
  (STATUS_USADO, "Cupon Usado"),
)


class Localizacao(models.Model):
    """
     Localizacoes
    """
    class Meta:
        db_table = 'localizacao'
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'

    cidade  = models.CharField(verbose_name=_("Nome da Cidade"), max_length=60,default='goiania')
    estado  = models.CharField(verbose_name=_("Nome do Estado"), max_length=60,default='goias')
    cep     = models.CharField(max_length=7,blank=True,default='123456')
    slug    = models.SlugField(db_index=True,default='goiania')
    ativo   = models.BooleanField(default=True, db_index=True)

    def __unicode__(self):
        return self.cidade

    def get_absolute_url(self):
        return reverse('cidade_index', kwargs={'cidade_slug': self.pk})

class Anunciante(models.Model):
    """
     Cliente Anunciante
    """
    class Meta:
        db_table = 'anunciantes'
        verbose_name = _('Anunciante')
        verbose_name_plural = _('Anunciantes')

    nome            = models.CharField(max_length=60,default='Restaurante ')
    endereco        = models.CharField(max_length=60,default='Rua da ')
    localizacao     = models.ForeignKey(Localizacao)
    telefone        = models.CharField(max_length=25,default='12345678 ')
    telefone_extra  = models.CharField("Telefone Extra", max_length=6, blank=True,default='123456 ')
    celular         = models.CharField(max_length=25,default='1234566 ')
    fax             = models.CharField(max_length=25,default='123466 ')
    contato         = models.CharField(max_length=50, blank=True, help_text="Contato com o anunciante",default='pessoa de contato ')
    email           = models.EmailField(blank=True, help_text="Email do contato",default='a@a.com  ')
    website         = models.URLField(blank=True, verbose_name=_('Website'),default='www.anunciante.com ')
    latitude        = models.DecimalField(
                        verbose_name=_("Latitude (decimal)"),
                        max_digits=9,
                        decimal_places=6,
                        blank=True,
                        null=True,
                        default='-16.671 '
                        )
    longitude       = models.DecimalField(
                        verbose_name=_("Longitude (decimal)"),
                        max_digits=9,
                        decimal_places=6,
                        blank=True,
                        null=True,
                        default='-49.235 '
                        )

    def __unicode__(self):
        return self.nome
    class Admin:
        list_display = ( "nome", "contato", "email", "telefone" )

class Categoria(models.Model):
    class Meta:
        db_table = 'categorias'
        ordering = ['-nome']
        verbose_name_plural = 'Categorias'
        
    nome                = models.CharField(max_length=50,default='Restaurante ')
    slug                = models.SlugField(max_length=50, unique=True,
                            help_text=u'Valor unico para a URL da pagina do produto, criado a partir do nome.')
    descricao           = models.TextField(default='Descricao categoria ')
    ativo               = models.BooleanField(default=True)
    meta_keywords       = models.CharField("Meta Keywords",max_length=255,
                                     help_text=u'Conjunto delimitado por virgulas de palavras-chave para SEO meta tag',default='Restaurante ')
    meta_description    = models.CharField("Meta Description", max_length=255,
                                        help_text=u'Descricao da meta-tag',default='Restaurante descricao')
    criado_em           = models.DateTimeField(auto_now_add=True)
    atualizado_em       = models.DateTimeField(auto_now=True)
   
   
    def __unicode__(self):
        return self.nome
    
    @ models.permalink
    def get_absolute_url(self):
        return (u'catalogo_categoria', (), { u'categoria_slug': self.slug })

class Cupon(models.Model):
    """
    Cupon
    """
    class Meta:
        db_table = 'cupons'
        verbose_name = _('Cupon')
        verbose_name_plural = _('Cupons')

    #objects = _default_manager = OfertaManager()

    anunciante               = models.ForeignKey(Anunciante)
    cidade                   = models.ForeignKey(Localizacao, related_name='cupons')
    titulo                   = models.CharField(verbose_name=_("Titulo"), max_length=256,default='Restaurante ')
    subtitulo                = models.CharField(verbose_name=_("SubTitulo"), max_length=256,default='Cupon com desconto ')
    
    slug                     = models.SlugField(db_index=True)

    categoria                = models.ForeignKey(Categoria)
    
    valor_real               = models.DecimalField(decimal_places=2, max_digits=6, help_text='Valor de base para a Oferta',default=100)#default=0,
    valor_desconto           = models.DecimalField(decimal_places=2, max_digits=6, help_text='Valor do desconto em Reais',default=20)#default=0,
    
    destaque                 = models.BooleanField(default=False, db_index=True)
    ativo                    = models.BooleanField(default=True, db_index=True)    

    qtd_ofertas_disponiveis  = models.IntegerField(default=1000)
    qtd_ofertas_por_pessoa   = models.IntegerField(default=3)
    qtd_ofertas_adquiridas   = models.IntegerField(default=1)


    sobre_oferta             = models.TextField(default='sobre Restaurante ',blank=True)
    destaque_oferta          = models.TextField(default='desque do cupon de Restaurante ',blank=True)
    descricao_completa       = models.TextField(default='descricao completa Restaurante ',blank=True)
    descricao_resumida       = models.TextField(default='descricao resumida Restaurante ',blank=True)
   
    imagem                   = models.ImageField(upload_to='cupon_imagems/', blank=True)
    miniatura                = models.ImageField(upload_to='cupon_mini/', blank=True)
 
    meta_keywords            = models.CharField("Meta Keywords", max_length=255,
                                     help_text=u'Conjunto delimitado por virgulas de palavras-chave para SEO meta tag',default='Restaurante ')
    meta_description         = models.CharField("Meta Description", max_length=255,
                                        help_text=u'Descricao da meta-tag',default='Restaurante descricao meta')


    latitude        = models.DecimalField(
                        verbose_name=_("Latitude (decimal)"),
                        max_digits=9,
                        decimal_places=6,
                        blank=True,
                        null=True,
                        default='-16.671 '
                        )
    longitude       = models.DecimalField(
                        verbose_name=_("Longitude (decimal)"),
                        max_digits=9,
                        decimal_places=6,
                        blank=True,
                        null=True,
                        default='-49.235 '
                        )
    
    data_entrada             = models.DateTimeField(blank=True, editable=False, null=True, auto_now_add=True)
    data_modificacao         = models.DateTimeField(blank=True, editable=False, null=True, auto_now=True)
    
    def __unicode__(self):
        return self.titulo
    
    @property
    def num_disponivel(self):
        cupons_ativos = Cupon.objects.filter(id=self.id,ativo=True).count()
        num_disponivel = self.qtd_ofertas_disponiveis - cupons_ativos
        return num_disponivel
    
    @property
    def cupons_ativos(self):
        qtd_cupons_ativos = Cupon.objects.filter(id=self.id,ativo=True).count()
        return qtd_cupons_ativos
    
    @property
    def porcentagem_vendido(self):
        num_vendido = self.cupons_ativos
        if num_vendido > self.qtd_ofertas_disponiveis:
            return 100
        elif self.qtd_ofertas_disponiveis:
            return int( ( (num_vendido*1.0) / self.qtd_ofertas_disponiveis) * 100)
        else:
            return 0
        
    @property
    def desconto(self):
        """Porcentagem de desconto"""
        diferenca= self.valor_real-self.valor_desconto
        aux=diferenca*100
        return aux/self.valor_real
    
    @property
    def desconto_valor(self):
        """Retorna a diferenca do valor real com desconto"""
        return self.valor_real-self.valor_desconto
        
    def num_necessario_fechamento(self):
        qtd_cupons_ativos = self.cupons_ativos()
        if qtd_cupons_ativos > self.qtd_ofertas_disponiveis:
            return 0
        else:
            return self.qtd_ofertas_disponiveis - qtd_cupons_ativos
    
    @property
    def esta_expirado(self):
        qtd_cupons_ativos = Cupon.objects.filter(id=self.id,ativo=True).count()
        if qtd_cupons_ativos <= 0 :
            return True
        else:
            return False

    def get_absolute_url(self):
        return reverse('cupon_detalhes', kwargs={'cidade_slug': self.cidade.slug, 'cupon_slug': self.slug})

    def get_checkout_url(self):
        return reverse('cupon_checkout', kwargs={'cidade_slug': self.cidade.slug, 'cupon_slug': self.slug})

    def get_endereco_completo(self):
        return ','.join(filter(bool, [self.anunciante.endereco, self.anunciante.cidade.nome]))

    def get_telefones(self):
        return ','.join(filter(bool, [self.anunciante.telefone, self.anunciante.telefone_extra]))


class Cupon_Adquirido(models.Model):
    class Meta:
        db_table = 'cupons_adquiridos'
        verbose_name = _('Cupon adquirido')
        verbose_name_plural = _('Cupons adquiridos')

    usuario                = models.ForeignKey(User)
    cupon                  = models.ForeignKey(Cupon)
    status                 = models.IntegerField(choices=STATUS, default=0, db_index=True)
    data_entrada           = models.DateTimeField(blank=True, editable=False, null=True, auto_now_add=True)
    data_modificacao       = models.DateTimeField(blank=True, editable=False, null=True, auto_now=True)
    data_exclusao          = models.DateTimeField(blank=True, editable=False, null=True)

    def __unicode__(self):
        return str(self.usuario)
    
class Cadastra_Email(models.Model):
    class Meta:
        db_table = 'emails'
        verbose_name = _('Email Cadastrado')
        verbose_name_plural = _('Emails Cadastrados')
    
    email           = models.EmailField(blank=True, help_text="Digite seu e-mail",default='Digite seu e-mail')

# SIGNALS
#from django.db.models import signals
#
#def cupon_pre_save(instance, **kwargs):
#    
##    if instance.finaliza_em and instance.inicia_em:
##        delta = (instance.finaliza_em - instance.inicia_em)
##        instance.duracao_da_oferta = (delta.days * 24) + (delta.seconds / 60 / 60)
##    elif instance.inicia_em and instance.duracao_da_oferta and not instance.finaliza_em:
##        instance.finaliza_em = instance.inicia_em + datetime.timedelta(seconds=instance.duracao_da_oferta * 60 * 60)
#
#signals.pre_save.connect(cupon_pre_save, sender=Cupon)
