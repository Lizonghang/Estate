# coding=utf-8
from django.http import JsonResponse, HttpResponse


def handler500(request):
    return JsonResponse({'err': 1, 'msg': u'未知错误,请检查数据提交方法和参数是否正确'})


def index(request):
    return HttpResponse('index page')
