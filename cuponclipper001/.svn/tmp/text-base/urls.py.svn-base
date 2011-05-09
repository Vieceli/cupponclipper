from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from cuponclipper001 import settings

admin.autodiscover()
#admin.site.unregister(User)

urlpatterns = patterns('',
    #INDEX         
    url(r'^$', 'cuponclipper001.cupon.views.index', name='index'),

    (r'^(robots.txt)$', 'django.views.static.serve', {'document_root': '/var/www/massivecoupon/'}),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       
     #includes
    (r'^cupons/', include('cupon.urls')),
    (r'^conta/', include('contas.urls')),
    (r'^boleto/', include('boleto.urls')),#inseria midia propria -->url(r'imagem_barras/$', imagem_barras, name='imagem_barras'),
    (r'^conta/', include('django.contrib.auth.urls')),
    url(r'imagem_barras/$', 'cuponclipper001.boleto.views.imagem_barras', name='imagem_barras'),
   
)

if settings.LOCAL:
    urlpatterns = urlpatterns + patterns('',
        ((r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT})),
                                         
        )
#    
handler404 = 'cuponclipper001.views.file_not_found_404'
handler500 = 'cuponclipper001.views.server_error_500'