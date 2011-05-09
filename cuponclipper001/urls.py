from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from cuponclipper001 import settings

admin.autodiscover()
#admin.site.unregister(User)

urlpatterns = patterns('',
                       
    url(r'^$', 'cuponclipper001.cupon.views.index', name='index'),

    (r'^(robots.txt)$', 'django.views.static.serve', {'document_root': '/var/www/massivecoupon/'}),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       
     #includes
    (r'^cupons/', include('cuponclipper001.cupon.urls')),
    (r'^conta/', include('contas.urls')),
    (r'^conta/', include('django.contrib.auth.urls')),
)

if settings.LOCAL:
    urlpatterns = urlpatterns + patterns('',
        ((r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT})),
        )
#    
handler404 = 'cuponclipper001.views.file_not_found_404'
handler500 = 'cuponclipper001.views.server_error_500'