# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_GET, require_POST
from WXMsgHandler import WXMsgHandler
from django.contrib import auth
from .models import *
import config
import hashlib
import requests
import uuid
import wxtools


def handler500(request):
    return JsonResponse({'err': 1, 'msg': u'请检查数据提交方法和参数是否正确'})


def login_require(request):
    return JsonResponse({'err': 1, 'msg': u'该操作需要登录状态'})


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
    session, _ = SessionToken.objects.get_or_create(user=user)
    session.token = wxtools.get_md5(str(uuid.uuid1()))
    session.save()

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
    params['token'] = session.token
    for key in params.keys():
        url = url + '{key}={value}'.format(key=key, value=params[key]) + '&'
    url = url[:-1]
    print u'页面跳转: ' + url
    return HttpResponseRedirect(url)


@require_GET
def login(request):
    token = request.GET.get('token')
    session = SessionToken.objects.get(token=token)
    user = session.user
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth.login(request, user)
    return JsonResponse({'err': 0})


@require_GET
def banner(request):
    banner_info = [image.get_image_url() for image in Banner.objects.all()]
    return JsonResponse({'err': 0, 'data': banner_info})


@login_required
@require_POST
def repair(request):
    params = request.POST
    loc = params.get('loc')
    desc = params.get('desc')
    user = request.user

    Repair.objects.create(user=user, loc=loc, desc=desc)

    return JsonResponse({'err': 0})


@require_GET
def activities(request):
    activity_list = []
    for activity in Activity.objects.all():
        activity_list.append(activity.get_base_info())
    return JsonResponse({'err': 0, 'data': activity_list})


@login_required
@require_POST
def join(request):
    name = request.POST.get('name')
    user = request.user
    print name
    print user
    activity = Activity.objects.get(name=name)
    log, new = JoinUser.objects.get_or_create(user=user, activity=activity)
    if not new:
        return JsonResponse({'err': 1, 'msg': '您已报名该活动'})
    activity.join = len(JoinUser.objects.filter(activity=activity))
    activity.save()
    return JsonResponse({'err': 0})


@login_required
@require_POST
def message(request):
    msg = request.POST.get('message')
    user = request.user

    MessageBoard.objects.create(user=user, message=msg)

    return JsonResponse({'err': 0})


@login_required
@require_POST
def bind(request):
    params = request.POST
    name = params.get('name')
    room = params.get('room')
    user = request.user
    user_info, _ = UserInfo.objects.get_or_create(user=user)
    user_info.name = name
    user_info.room = room
    user_info.save()
    return JsonResponse({'err': 0})


@login_required
@require_GET
def payinfo(request):
    info = request.user.payment_set.get(date=default_month_now()).get_pay_info()
    return JsonResponse({'err': 0, 'data': info})


@login_required
@require_POST
def pay(request):
    try:
        pay = request.user.payment_set.get(date=default_month_now())
    except ObjectDoesNotExist:
        return JsonResponse({'err': 1, 'msg': u'当月没有待缴费的费用'})
    pay.paid = True
    pay.save()
    return JsonResponse({'err': 0})


@require_GET
def places(request):
    place_list = [item.get_place_info() for item in Rent.objects.all() if not item.rented]
    return JsonResponse({'err': 0, 'data': place_list})


@login_required
@require_POST
def rent(request):
    place = request.POST.get('place')
    user = request.user

    try:
        rent = Rent.objects.get(place=place)
    except ObjectDoesNotExist:
        return JsonResponse({'err': 1, 'msg': u'该场地不在出租列表中'})

    rent.user = user
    rent.rented = True
    rent.save()
    return JsonResponse({'err': 0})


def refresh_place(request):
    for item in Rent.objects.all():
        item.user = None
        item.rented = False
        item.save()
    return HttpResponse()


@require_GET
def drinks(request):
    drink_info = [item.get_base_info() for item in Drink.objects.all()]
    return JsonResponse({'err': 0, 'data': drink_info})


@login_required
@require_POST
def drinkorder(request):
    params = request.POST
    name = params.get('name')
    loc = params.get('loc')
    user = request.user

    try:
        drink = Drink.objects.get(name=name)
    except ObjectDoesNotExist:
        return JsonResponse({'err': 1, 'msg': u'该饮品未销售'})

    DrinkOrder.objects.create(user=user, drink=drink, loc=loc)
    return JsonResponse({'err': 0})


@require_GET
def lose(request):
    lose_info = [item.get_base_info() for item in LoseAndFound.objects.all() if not item.state]
    return JsonResponse({'err': 0, 'data': lose_info})
