# Create your views here.
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, Http404
from cuponclipper001 import settings
from django.shortcuts import get_object_or_404, render_to_response
from cuponclipper001.cupon.models import Localizacao, Cupon, Cupon_Adquirido,\
    STATUS_EM_ESPERA, Cadastra_Email
from django.template.context import RequestContext
#geoip
from django.contrib.gis.utils import GeoIP
from gmapi import maps
from cuponclipper001.cupon.forms import MapForm, OfertaCheckoutForm, FormBuscar,\
    FormCadEmail
from django.contrib.auth.models import User
from cuponclipper001.contas.models import MeuUser
from django.contrib.auth import authenticate
from django.contrib.auth.views import login

def index(request):
    return HttpResponseRedirect(settings.DEFAULT_CITY_SLUG)
#           #tratamento do ajax
#           if ajax:
#                variaveis = RequestContext(request, {
#                    'bookmarks': [bookmark],
#                    'show_edit': True,
#                    'show_tags': True
#                    })
#                return render_to_response('lista_bookmark.html', variaveis)
#           else:
#                return HttpResponseRedirect('/usuario/%s/' % request.user)
#        else:
#            if ajax:
#                return HttpResponse(u'falha')
#    
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
    
   
    
    #EMAIL FORM_EMAIL
    form_email = FormCadEmail()
    email_cadastrado = False
#    if request.method == 'POST':
#        form_email = FormCadEmail(request.POST)
#        if form_email.is_valid():
#           cd = form_email.cleaned_data
#           print (email_cadastrado)
#           print "email"
#           email_cadastrado = True
#           cad_email=Cadastra_Email()
#           cad_email.email = cd.get('email')
#           cad_email.save()
           
     #BUSCA FORM_BUSCA
    form_busca = FormBuscar()
    cupons_busca_titulo = []
    resultados = False
    if 'query' in request.GET:
        resultados = True
        query = request.GET['query'].strip()
        if query:
            form_busca = FormBuscar({'query' : query})#Usado para manter o valor do campo no formulario quando atualizar
            cupons_busca_titulo = Cupon.objects.filter(
            titulo__icontains=query
            )[:10]
    elif 'email' in request.GET:
        form_email = FormCadEmail(request.GET)
        if form_email.is_valid():
           cd = form_email.cleaned_data
           print (email_cadastrado)
           print "email"
           email_cadastrado = True
           cad_email=Cadastra_Email()
           cad_email.email = cd.get('email')
           cad_email.save()

            
    context = {'cidade_cliente': cidade_cliente,
               'form_busca':form_busca,
               'form_email': form_email,
               'email_cadastrado':email_cadastrado,
                'cupons_busca_titulo': cupons_busca_titulo,
                'resultados': resultados,                
#                'show_tags': True,                
#                'show_user': True,
                'cupons' : cupons,
                'destaque' : destaque,
                'meta_keywords' : meta_keywords,
                'meta_description' : meta_description,
                'usuario' : usuario,
                'cidades_disponiveis': cidades_disponiveis,}
    
    

    
    if request.GET.has_key('ajax'):
        print context
        return render_to_response('listar_cupons_busca.html', context)
    else:
        print context
        return render_to_response('index.html', context)
    
    #return render_to_response('index.html',context)
     
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
    usuario=request.user
    user_msg = ""
    try:
        cupon = Cupon.objects.get(slug=cupon_slug)
    except:
        return HttpResponseRedirect('/')

    must_login_error = False
    must_login_email = None
    maximo = cupon.qtd_ofertas_por_pessoa # maxima quantidade para cada cliente
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
              
            except:
                #return HttpResponseRedirect('/')
                pass
                
        else:
            user = request.user
        #if not must_login_error and form.is_valid():
#        quantidade = request.POST.get('quantidade', '')
#        print quantidade
        if not must_login_error and form.is_valid():
            cd = form.cleaned_data
            if not request.user.is_authenticated():
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

        quantidade = int(request.POST.get('quantidade', ''))#pega o conteudo pelo nome do elemento dom
        print quantidade
        preco_total = quantidade * cupon.valor_desconto

    else:
        form = OfertaCheckoutForm(lista=lista)
        usuario=request.user

    cidades = Localizacao.objects.filter(ativo=True)

    return render_to_response('oferta/oferta_checkout.html', {
                'form' : form,
                'cupon' : cupon,
                'user_msg' : user_msg,
                'must_login_error' : must_login_error,
                'must_login_email' : must_login_email,
                'cidades' : cidades,
                'usuario' : usuario,
              }, context_instance=RequestContext( request ) )

def cupon_checkout_complete(request, cupon_slug, quantidade):

    user_msg = ""
    quantidade = int(quantidade)

    try:
        cupom = Cupon.objects.get(cupon_slug=cupon_slug)
    except:
        return Http404()

    #cupom.qtd_ofertas_adquiridas+=quantidade

      # check if it's sold out!
    if cupom.qtd_ofertas_adquiridas >= cupom.qtd_ofertas_disponiveis:
        print "oferta vendida"
        #setup form error
        # Sold out!


        for i in range(quantidade):
            cupon_adquirido = Cupon_Adquirido()
            cupon_adquirido.user = request.user
            cupon_adquirido.cupon = cupon_adquirido
    
            cupon_adquirido.status = STATUS_EM_ESPERA
    
            cupon_adquirido.save()
            cupom.qtd_ofertas_adquiridas +=1
            
            cupon_adquirido.save()
        # update the deal object 
#        if not deal.is_deal_on and num_sold >= deal.tipping_point:
#          deal.tipped_at = datetime.datetime.now()
#          deal.is_deal_on = True
#          deal.save()


        user_msg = 'Thanks for purchasing a Massive Coupon! It will arrive in your profile within 24 hours'
        return HttpResponseRedirect('/deals/groupon-clone/?user_msg=' + user_msg )
#    else:
#      return Http404()

    else:
        return Http404()

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

def cadastra_email(request,form):
     #geo
    ip_address=request.META.get('REMOTE_ADDR') 
    g = GeoIP()
    #local_full_cliente = g.city(ip_address)
    local_full_cliente = g.city('201.22.164.216')
    cidade_cliente = local_full_cliente.get('city')
    uni = cidade_cliente.decode('cp1252')
    cidade_cliente = uni.encode('utf8')
    return cidade_cliente
