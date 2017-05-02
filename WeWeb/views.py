# coding=utf-8
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_GET, require_POST
from WXMsgHandler import WXMsgHandler
from django.contrib import auth
from .models import *
import config
import hashlib
import requests


def handler500(request):
    return JsonResponse({'err': 1, 'msg': u'未知错误,请检查数据提交方法和参数是否正确'})


def index(request):
    return HttpResponse('index page')


def server_access(request):
    token = config.wxToken
    params = request.GET
    args = [token, params['timestamp'], params['nonce']]
    args.sort()
    if hashlib.sha1("".join(args)).hexdigest() == params['signature']:
        if 'echostr' in params:
            return HttpResponse(params['echostr'])
        if request.method == 'POST':
            handler = WXMsgHandler(request, token, params)
            encrypt_xml = handler.event_router()
            return HttpResponse(encrypt_xml)
    return HttpResponse()


@require_GET
def authorize(request):
    code = request.GET.get('code', '')
    state = request.GET.get('state', '')
    appid = config.wxAppID
    appsecret = config.wxAppSecret
    api = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (appid, appsecret, code)

    try:
        openid = requests.get(api).json().get('openid')
    except Exception:
        return HttpResponse()

    user, new = User.objects.get_or_create(username=openid)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth.login(request, user)

    # 从state参数中取出url与自定义键值对,并生成合法的带查询参数的重定向url
    url = ''
    raw_kvPairs = state.split(',')
    params = {}
    for pair in raw_kvPairs:
        key, value = pair.split('=')
        if key == 'url':
            url = value.replace('', '#')
        else:
            params[key] = value

    if not url:
        return JsonResponse({'err': 1, 'msg': u'参数没有提供url'})

    url += '?'
    for key in params.keys():
        url = url + '{key}={value}'.format(key=key, value=params[key]) + '&'
    url = url[:-1]
    print u'Redirect to url: ', url
    return HttpResponseRedirect(url)
