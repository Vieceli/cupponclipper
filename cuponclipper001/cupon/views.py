# Create your views here.
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, Http404
from cuponclipper001 import settings
from django.shortcuts import get_object_or_404, render_to_response
from cuponclipper001.cupon.models import Localizacao, Cupon, Cupon_Adquirido,STATUS_EM_ESPERA, Cadastra_Email
from django.template.context import RequestContext
#geoip
from django.contrib.gis.utils import GeoIP
from gmapi import maps
from cuponclipper001.cupon.forms import MapForm, OfertaCheckoutForm, FormBuscar,FormCadEmail
from django.contrib.auth.models import User
from cuponclipper001.contas.models import MeuUser
from django.contrib.auth import authenticate
from django.contrib.auth.views import login
from cuponclipper001.pagseguro.pagseguro import Pagseguro

def index(request):
    return HttpResponseRedirect(settings.DEFAULT_CITY_SLUG)

def cidade_index(request, cidade_slug):
    usuario=request.user
    cidade = get_object_or_404(Localizacao, slug=cidade_slug,ativo=True)
    cidades_disponiveis = Localizacao.objects.filter(ativo=True)
    cupons = Cupon.objects.filter(cidade=cidade,ativo=True)[:8] 
    destaque = Cupon.objects.filter(cidade=cidade,ativo=True,destaque=True)[:4]   
    cidade_cliente=_cidade_cliente(request)

    meta_keywords = settings.META_KEYWORDS
    meta_description = settings.META_DESCRIPTION
           
    #BUSCA FORM_BUSCA
    form_busca = FormBuscar()
          
    #EMAIL FORM_EMAIL
    form_email = FormCadEmail()
    email_cadastrado = False  
    email_duplicado=False     
    if request.method == 'POST':
        postdata = request.POST.copy()
        form_email = FormCadEmail(postdata)
        if form_email.is_valid():
                cd = form_email.cleaned_data  
                cad_email=Cadastra_Email()
                cad_email.email = cd.get('email')
                cad_email.cidade = cidade_cliente
                cad_email.save()
                email_cadastrado = True
   
    context = {'cidade_cliente': cidade_cliente,
               'form_busca':form_busca,
               'form_email': form_email,
               'email_cadastrado':email_cadastrado,
               'cupons' : cupons,
               'destaque' : destaque,
               'meta_keywords' : meta_keywords,
               'meta_description' : meta_description,
               'usuario' : usuario,
               'cidades_disponiveis': cidades_disponiveis,}

    return render_to_response('index.html', context, context_instance=RequestContext(request))

def buscar(request,cidade_slug):
    usuario=request.user
    cidade_cliente=_cidade_cliente(request)
    cidades_disponiveis = Localizacao.objects.filter(ativo=True)
    
    #BUSCA FORM_BUSCA
    form_busca = FormBuscar()
    cupons_busca_titulo = []
    if 'query' in request.GET:
        query = request.GET['query'].strip()
        if query:
            form_busca = FormBuscar({'query' : query})#Usado para manter o valor do campo no formulario quando atualizar
            cupons_busca_titulo = Cupon.objects.filter(titulo__icontains=query)[:10]
    
  
    mat=[]
 
    for cidade in cidades_disponiveis:
        qtd_cupons = Cupon.objects.filter(cidade=cidade,ativo=True).count()
        mat.append(str(qtd_cupons))
    
    context = {'form_busca':form_busca,
               'cupons_busca_titulo': cupons_busca_titulo,
               'cidade_cliente': cidade_cliente,              
               'usuario' : usuario,
               'cidades_disponiveis': cidades_disponiveis,
               'mat':mat,
               }

    return render_to_response('oferta/buscar.html', context, context_instance=RequestContext(request))
     
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
    
    form_busca = FormBuscar()
    context = {'form': MapForm(initial={'map': gmap}),
               'user_msg' : user_msg,
                'cupom' : cupom,
#                'porcentagem_vendido': porcentagem_vendido,
#                'desconto': desconto,
                'form_busca':form_busca,
                'cidade_cliente': cidade_cliente,
                'cidades_disponiveis': cidades_disponiveis,}
    
    return render_to_response('oferta/oferta_detalhes.html', context)

def cupon_checkout(request, cidade_slug, cupon_slug):
    usuario=request.user
    cidade_cliente=_cidade_cliente(request)
    cidades = Localizacao.objects.filter(ativo=True)
    
    form_busca = FormBuscar()
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
        print request.user.is_authenticated()
        # Se o usuario nao estiver autenticado
        if not request.user.is_authenticated():
            try:
                #user = MeuUser.objects.get(email=request.POST.get('username', ''))
                usuario = authenticate(username=request.POST.get('username', ''), password=request.POST.get('password', ''))
                print usuario
                must_login_error = True
                must_login_email = request.POST['email']
                
                form = OfertaCheckoutForm(lista=lista)
                user_msg = 'A conta existe: ' + usuario.email  + '. Efetue Login.'

            except Exception as erro:
                #return HttpResponseRedirect('/')
                print 'My exception occurred, value:', erro
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
        #o preco do cupon nao eh lido pelo ajax
        print quantidade
        preco_total = quantidade * cupon.valor_desconto
        
#        carrinho = Pagseguro(email_cobranca='pagseguro@visie.com.br',tipo='CP')
#        carrinho.item(id=1, descr='Um produto de exemplo', quant=5, valor=10)
#        carrinho.item(id=2, descr='Outro produto de exemplo', quant=2, valor=100)
#        print carrinho.mostra()
        
        #token=7FCE5D68A80346CF8713F3A4E27D3CF8
    else:
        form = OfertaCheckoutForm(lista=lista)
        usuario=request.user


    return render_to_response(
                'oferta/oferta_checkout.html',{
                'cidade_cliente': cidade_cliente,
                'form_busca':form_busca,
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


