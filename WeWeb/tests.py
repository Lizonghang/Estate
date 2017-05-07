# encoding: utf-8
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from .models import *


def login(request):
    openid = request.GET.get('openid', '')
    user = User.objects.get(username=openid)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth.login(request, user)
    return HttpResponse(u'登录成功')


def logout(request):
    auth.logout(request)
    return HttpResponse(u'注销成功')


def whoami(request):
    return JsonResponse({'user': request.user.username})
