# encoding: utf-8
from django.conf.urls import include, url
from WeWeb import views, tests

test_map = [
    url(r'login/$', tests.login),
    url(r'logout/$', tests.logout),
]

urlpatterns = [
    url(r'^$', views.index),
    url(r'access/$', views.server_access),
    url(r'authorize/$', views.authorize),
    url(r'repair/$', views.repair),
    url(r'test/', include(test_map)),
]
