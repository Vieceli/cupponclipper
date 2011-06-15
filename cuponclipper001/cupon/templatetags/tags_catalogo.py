from django import template
from django.contrib.flatpages.models import FlatPage
from cuponclipper001.cupon.models import Localizacao, Cupon


register = template.Library()


@register.inclusion_tag("tags/lista_de_cidades_busca.html")
def lista_cidades_busca():
    cidades_disponiveis = Localizacao.objects.filter(ativo=True)
    cupons = Cupon.objects.filter(ativo=True)
    
    num_cupons=[]
    cidades_cupons=[]
    for i in cidades_disponiveis:
        cupons = Cupon.objects.filter(cidade=i,ativo=True).count()
        cidades_cupons.append(i)
        num_cupons.append(cupons)
    
    print num_cupons
    print cidades_cupons    
    return {
            'num_cupons':num_cupons,
            'cidades_cupons':cidades_cupons,
            }
    
@register.inclusion_tag("tags/rodape.html")
def links_rodape():
    flatpage_list = FlatPage.objects.all()
    return {'flatpage_list': flatpage_list }