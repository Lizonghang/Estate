# coding=utf-8
from django.http import JsonResponse, HttpResponse
from WXMsgHandler import WXMsgHandler
import config
import hashlib


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
