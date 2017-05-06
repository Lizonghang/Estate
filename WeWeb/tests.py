# encoding: utf-8
from django.http import HttpResponse
from django.contrib import auth
from .models import *


def login(request):
    openid = request.GET.get('openid', '')
    user = User.objects.get(username=openid)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth.login(request, user)
    return HttpResponse({'err': 0, 'sessionid': request.session.session_key})


def logout(request):
    auth.logout(request)
    return HttpResponse(u'注销成功')
