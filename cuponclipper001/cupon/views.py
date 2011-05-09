# Create your views here.
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from cuponclipper001 import settings
from django.shortcuts import get_object_or_404, render_to_response
from cuponclipper001.cupon.models import Localizacao, Cupon
from django.template.context import RequestContext
#geoip
from django.contrib.gis.utils import GeoIP
from gmapi import maps
from cuponclipper001.cupon.forms import MapForm, OfertaCheckoutForm
from django.contrib.auth.models import User
from cuponclipper001.contas.models import MeuUser
from django.contrib.auth import authenticate
from django.contrib.auth.views import login

def index(request):
    return HttpResponseRedirect(settings.DEFAULT_CITY_SLUG)

def cidade_index(request, cidade_slug):
#    up = MeuUser(username=request.user)
#    nome = up.username
    usuario=request.user
    cidade = get_object_or_404(Localizacao, slug=cidade_slug,ativo=True)
    cidades_disponiveis = Localizacao.objects.filter(ativo=True)
    cupons = Cupon.objects.filter(cidade=cidade,ativo=True)[:8] 
    destaque = Cupon.objects.filter(cidade=cidade,ativo=True,destaque=True)[:4]   
    cidade_cliente=_cidade_cliente(request)

    meta_keywords = settings.META_KEYWORDS
    meta_description = settings.META_DESCRIPTION
    
    context = {'cidade_cliente': cidade_cliente,
               'cidades_disponiveis' : cidades_disponiveis,
                'cupons' : cupons,
                'destaque' : destaque,
                'meta_keywords' : meta_keywords,
                'meta_description' : meta_description,
                'usuario' : usuario,
#                'nome' : nome,
                'cidades_disponiveis': cidades_disponiveis,}
    
    return render_to_response('index.html',context)
     
def cupon_detalhes(request, cidade_slug, cupon_slug):
    cidade = get_object_or_404(Localizacao, slug=cidade_slug)
    cidades_disponiveis = Localizacao.objects.filter(ativo=True)
    cupom = get_object_or_404(Cupon, slug=cupon_slug)
    cidade_cliente=_cidade_cliente(request)
    
    #pega a mensagem da url
    try:
        user_msg = request.GET.get('user_msg', None)
    except:
        user_msg = None
    
    #Mapa
    gmap = maps.Map(opts = {
        'center': maps.LatLng(cupom.latitude, cupom.longitude),
        'mapTypeId': maps.MapTypeId.ROADMAP,
        'zoom': 15,
        'mapTypeControlOptions': {
             'style': maps.MapTypeControlStyle.DROPDOWN_MENU
        },
    })
    marker = maps.Marker(opts = {
        'map': gmap,
        'position': maps.LatLng(cupom.latitude, cupom.longitude),
    })
    maps.event.addListener(marker, 'mouseover', 'myobj.markerOver')
    maps.event.addListener(marker, 'mouseout', 'myobj.markerOut')
    info = maps.InfoWindow({
        'content': '<h3>'+cupom.anunciante.nome+'</h3>'+
                   '<p>Rua: '+cupom.anunciante.endereco+'</p>'+
                   '<p>Telefone: '+cupom.anunciante.telefone+'</p>',
        'disableAutoPan': False
    })
    info.open(gmap, marker)
    
    context = {'form': MapForm(initial={'map': gmap}),
               'user_msg' : user_msg,
                'cupom' : cupom,
#                'porcentagem_vendido': porcentagem_vendido,
#                'desconto': desconto,
                'cidades_disponiveis': cidades_disponiveis,}
    
    return render_to_response('oferta/oferta_detalhes.html', context)

def cupon_checkout(request, cidade_slug, cupon_slug):
   
    user_msg = ""
    try:
        oferta = Cupon.objects.get(slug=cupon_slug)
    except:
        return HttpResponseRedirect('/')

    must_login_error = False
    must_login_email = None
    maximo = oferta.qtd_ofertas_por_pessoa # maxima quantidade para cada cliente
    maximo = list(range(1,maximo+1))       # transforma essa quantidade numa lista
    lista = [(str(i), i) for i in maximo]  # transforma numa lista de dicionarios
    
    if request.method == 'POST': # If the form has been submitted...
        form = OfertaCheckoutForm(request.POST,lista=lista)

        # Se o usuario nao estiver autenticado
        if not request.user.is_authenticated():
            try:
                user = MeuUser.objects.get(email=request.POST['email'])
                must_login_error = True
                must_login_email = request.POST['email']
                form = OfertaCheckoutForm(lista=lista)
                user_msg = 'A conta existe: ' + user.email  + '. Efetue Login.'
                usuario=request.user
            except:
                #return HttpResponseRedirect('/')
                pass
                
        else:
            user = request.user
#Se native erro no formulario e o formulario for valido 
        #if not must_login_error and form.is_valid():
        if form.is_valid():
            cd = form.cleaned_data
            if not request.user.is_authenticated():
                # User in NOT Logged IN and doesn't exist
                # setup a new user
                cd = form.cleaned_data
                username = request.POST.get('email', '')
                password = request.POST.get('senha1', '')
                email = request.POST.get('email', '')
                user = MeuUser.objects.create_user(username, email, password);
                user.save()
                user.first_name = request.POST.get('nome', '')
                user.last_name = request.POST.get('sobrenome', '')
                user.cpf = request.POST.get('cpf', '')
                user.telefone = request.POST.get('telefone', '')
                user.save()
                form.envia_email() ################### enviar email 
                if user is not None:
                    if user.is_active:
                        novo_usuario = authenticate(username=user.email, password=cd.get('senha1'))
                        # Redirect to a success page.
                    else:
                        pass
                        # Return a 'disabled account' error message
                else:
                    # Return an 'invalid login' error message.
                    pass

            quantidade = int(cd.get('quantidade'))#pega o conteudo pelo nome do elemento dom
            preco_total = quantidade * oferta.preco_oferta

    else:
        form = OfertaCheckoutForm(lista=lista)
        usuario=request.user

    cidades = Localizacao.objects.filter(ativo=True)

    return render_to_response('oferta/oferta_checkout.html', {
                'form' : form,
                'oferta' : oferta,
                'user_msg' : user_msg,
                'must_login_error' : must_login_error,
                'must_login_email' : must_login_email,
                'cidades' : cidades,
                'usuario' : usuario,
              }, context_instance=RequestContext( request ) )


def _cidade_cliente(request):
     #geo
    ip_address=request.META.get('REMOTE_ADDR') 
    g = GeoIP()
    #local_full_cliente = g.city(ip_address)
    local_full_cliente = g.city('201.22.164.216')
    cidade_cliente = local_full_cliente.get('city')
    uni = cidade_cliente.decode('cp1252')
    cidade_cliente = uni.encode('utf8')
    return cidade_cliente