from django.conf.urls.defaults import *
from cuponclipper001 import settings
from cuponclipper001.contas.views import logout_page


urlpatterns = patterns('cuponclipper001.contas.views',
	(r'^registro/$', 'registro', 
	    {'template_name': 'registration/registro.html', 'SSL': settings.ENABLE_SSL }, 'registro'),
	
	
	(r'^minha_conta/$', 'minha_conta', 
	 	{'template_name': 'registration/minha_conta.html'}, 'minha_conta'),			
#	(r'^pedido_info/$', 'pedido_info', 
#	 	{'template_name': 'registration/pedido_info.html'}, 'pedido_info'),
#					
#	r'^order_details/(?P<order_id>[-\w]+)/$', 'order_details', 
#	 	{'template_name': 'registration/order_details.html'}, 'order_details'),
#	(r'^login/$', 'mylogin',{'SSL': settings.ENABLE_SSL }, 'login'),
)

urlpatterns += patterns('django.contrib.auth.views',
	(r'^login/$', 'login', 
	 {'template_name': 'registration/login.html', 'SSL': settings.ENABLE_SSL }, 'login'),
	 (r'^logout/$',logout_page),
	
)	 