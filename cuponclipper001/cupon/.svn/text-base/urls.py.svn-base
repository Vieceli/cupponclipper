'''
Created on 28/04/2011

@author: jhoni
'''
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    
  
    
    url(r'^(?P<cidade_slug>\w+)/$', 'cuponclipper001.cupon.views.cidade_index', name='cidade_index'),
    url(r'^(?P<cidade_slug>\w+)/(?P<cupon_slug>[-\w]+)/$', 'cuponclipper001.cupon.views.cupon_detalhes',
        name='cupon_detalhes'),
    
#    url(r'^(?P<cidade_slug>\w+)/(?P<cupon_slug>[-\w]+)/(?P<quantidade>\d+)/checkout/completo/$',
#        'engine.views.oferta_checkout_complete', name='oferta_checkout_complete'),
                                     
    url(r'^(?P<cidade_slug>\w+)/(?P<cupon_slug>[-\w]+)/comprar/$',
        'cuponclipper001.cupon.views.cupon_checkout', name='cupon_checkout'),
)