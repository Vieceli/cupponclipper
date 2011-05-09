# Create your views here.
from cuponclipper001.contas.forms import FormularioRegistro#,PerfilUsuarioForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from cuponclipper001.contas import profile
from django.core import urlresolvers
from cuponclipper001.contas.models import MeuUser
from cuponclipper001.cupon.models import Localizacao

def registro(request, template_name="registration/registro.html"):
    cidades_disponiveis = Localizacao.objects.filter(ativo=True)
    """  Registra o Usuario """
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = FormularioRegistro(postdata)
        if form.is_valid():
            
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
            novo_usuario = authenticate(username=user.email, password=cd.get('senha1'))
            form.envia_email() ################### enviar email 
            if novo_usuario and novo_usuario.is_active:
                login(request, novo_usuario)
                url = urlresolvers.reverse('minha_conta')
                return HttpResponseRedirect(url) 
                #return HttpResponseRedirect('/registro/registrado/')
    else:
        form = FormularioRegistro()
        #form = PerfilUsuarioForm()
    page_title = 'Registro de Usuario'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
def logout_page(request):
    logout(request)

@login_required 
def minha_conta(request,template_name="registration/minha_conta.html"):
    cidades_disponiveis = Localizacao.objects.filter(ativo=True)
    try:
        #nome = request.user.username
        #perfil = profile.getPerfil(request.username)
        up = MeuUser(username=request.user)
        nome = up.username
        print "teste1"

    except:
        print "erro" 
        up = MeuUser(username=request.user)
        up.save()
        

#    if request.method == 'POST':
#        postdata = request.POST.copy()
#        #form = FormularioRegistro(postdata, instance=perfil)
#        form = FormularioRegistro(postdata, instance=up)
#        if form.is_valid():
            #profile.setPerfil(request)
#            form.save()
#            print "salvou"
#    else:
#        up = MeuUser(username=request.user)
#        #perfil = profile.getPerfil(request)
#        form = FormularioRegistro(instance=up)
#        #print perfil
#        print "teste2"

    return render_to_response('registration/minha_conta.html', locals(),
        context_instance = RequestContext(request))
    
    
#@login_required
#def pedido_info(request, template_name="registration/pedido_info.html"):
#    """ page containing a form that allows a customer to edit their billing and shipping information that
#    will be displayed in the order form next time they are logged in and go to check out """
#    if request.method == 'POST':
#        postdata = request.POST.copy()
#        form = PerfilUsuarioForm(postdata)
#        if form.is_valid():
#            profile.setPerfil(request)
#            url = urlresolvers.reverse('my_account')
#            return HttpResponseRedirect(url)
#    else:
#        user_profile = profile.getPerfil(request)
#        form = PerfilUsuarioForm(instance=user_profile)
#    page_title = 'Edit Order Information'
#    return render_to_response(template_name, locals(), context_instance=RequestContext(request))