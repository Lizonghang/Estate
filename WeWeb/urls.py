# encoding: utf-8
from django.conf.urls import include, url
from WeWeb import views

urlpatterns = [
    url(r'^$', views.index),
]
