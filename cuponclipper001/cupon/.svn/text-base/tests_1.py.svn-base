from django.http import HttpResponseRedirect
from cuponclipper001 import settings
from django.shortcuts import get_object_or_404, render_to_response
from cuponclipper001.cupon.models import Localizacao, Cupon
from django.template.context import RequestContext
#geoip
from django.contrib.gis.utils import GeoIP
from gmapi import maps
from cuponclipper001.cupon.forms import MapForm


cidade = get_object_or_404(Localizacao, slug='goiania')
cidades_disponiveis = Localizacao.objects.filter(ativo=True)
cupom = get_object_or_404(Cupon, slug='restaurante')

#teste de propriedades



