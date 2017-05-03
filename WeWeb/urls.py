# encoding: utf-8
from django.conf.urls import include, url
from WeWeb import views, tests

test_map = [
    url(r'login/$', tests.login),
    url(r'logout/$', tests.logout),
]

list_map = [
    url(r'activity', views.activities),
    url(r'place', views.places),
]

urlpatterns = [
    url(r'access/$', views.server_access),
    url(r'authorize/$', views.authorize),
    url(r'repair/$', views.repair),
    url(r'join/$', views.join),
    url(r'message/$', views.message),
    url(r'bind/$', views.bind),
    url(r'payinfo/$', views.payinfo),
    url(r'pay/$', views.pay),
    url(r'rent/$', views.rent),
    url(r'list/', include(list_map)),
    url(r'test/', include(test_map)),
    url(r'login_require/$', views.login_require),
    url(r'refresh_place/$', views.refresh_place),
]
