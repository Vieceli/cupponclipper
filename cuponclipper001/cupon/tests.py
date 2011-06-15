"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

            
#    elif 'email' in request.GET:
#        form_email = FormCadEmail(request.GET)
#        if form_email.is_valid():
#           cd = form_email.cleaned_data
#           print (email_cadastrado)
#           print "email"
#           email_cadastrado = True
#           cad_email=Cadastra_Email()
#           cad_email.email = cd.get('email')
#           cad_email.save()


#    cupons_busca_titulo = []
#    resultados = False
#    if 'query' in request.GET:
#        resultados = True
#        query = request.GET['query'].strip()
#        if query:
#            form_busca = FormBuscar({'query' : query})#Usado para manter o valor do campo no formulario quando atualizar
#            cupons_busca_titulo = Cupon.objects.filter(titulo__icontains=query)[:10]
  
  

   
#    #EMAIL FORM_EMAIL
#    form_email = FormCadEmail()
#    email_cadastrado = False       
#    if request.method == 'POST':
#        postdata = request.POST.copy()
#        form_email = FormCadEmail(postdata)
#        if form_email.is_valid():
#            cd = form_email.cleaned_data
#            print (email_cadastrado)
#            print "email"
#            email_cadastrado = True
#            cad_email=Cadastra_Email()
#            cad_email.email = cd.get('email')
#            cad_email.cidade = cidade_cliente
#            cad_email.save()
#
#
#
#if request.method == 'POST':
#        postdata = request.POST.copy()
#        form_email = FormCadEmail(postdata)
#        if form_email.is_valid():
#            cd = form_email.cleaned_data
#            print (email_cadastrado)
#            print "email"
#            email_cadastrado = True
#            cad_email=Cadastra_Email()
#            cad_email.email = cd.get('email')
#            cad_email.cidade = cidade_cliente
#            cad_email.save()
#mat2=[]
#mat=[]
#for cidade in cidades_disponiveis:
#    qtd_cupons = Cupon.objects.filter(cidade=cidade,ativo=True).count()   
#    mat.append(cidade.cidade)
#    mat.append(str(qtd_cupons))