from django.conf.urls import include, url
import xadmin
import settings
xadmin.autodiscover()

handler500 = 'WeWeb.views.handler500'

urlpatterns = [
    url(r'^backend/xadmin/', include(xadmin.site.urls)),
    url(r'^api/weweb/', include('WeWeb.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
]
