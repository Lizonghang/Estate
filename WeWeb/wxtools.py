# encoding: utf-8
import config
import requests
import json
import hashlib


def get_access_token():
    api = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}'.format(config.wxAppID, config.wxAppSecret)
    resp = requests.get(api).json()
    return resp['access_token']


def get_menu():
    api = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token=' + get_access_token()
    print requests.get(api).json()


def create_menu():
    api = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=' + get_access_token()
    index = config.authorize_uri % 'url=http://www.desckie.com/#/'.replace('#', '')
    fix = config.authorize_uri % 'url=http://www.desckie.com/#/Need-fix'.replace('#', '')
    pay = config.authorize_uri % 'url=http://www.desckie.com/#/Pay'.replace('#', '')
    message = config.authorize_uri % 'url=http://www.desckie.com/#/Message'.replace('#', '')

    menu = """{
        "button": [
            {
                "url": "%s",
                "type": "view",
                "name": "小区首页"
            },
            {
                "name": "快捷服务",
                "sub_button": [
                    {
                        "url": "%s",
                        "type": "view",
                        "name": "物业报修"
                    },
                    {
                        "type": "click",
                        "name": "访客预约",
                        "key": "fangkeyuyue"
                    },
                    {
                        "url": "%s",
                        "type": "view",
                        "name": "物业缴费"
                    },
                    {
                        "url": "%s",
                        "type": "view",
                        "name": "留言板"
                    }
                ]
            }
        ]
    }""" % (index, fix, pay, message)
    print requests.post(api, menu).text


def send_template_message(data):
    api = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + get_access_token()
    resp = requests.post(api, data=json.dumps(data)).json()
    return resp


def get_md5(str):
    h = hashlib.md5()
    h.update(str)
    return h.hexdigest()

