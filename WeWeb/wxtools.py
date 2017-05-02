# encoding: utf-8
import config
import requests


def get_access_token():
    api = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}'.format(config.wxAppID, config.wxAppSecret)
    resp = requests.get(api).json()
    return resp['access_token']


def get_menu():
    api = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token=' + get_access_token()
    print requests.get(api).json()


def create_menu():
    api = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=' + get_access_token()
    index = config.authorize_uri % 'url=https://www.elongway.com/#/'.replace('#', '')
    menu = """{
        "button": [
            {
                "type": "view",
                "name": "合同实用指南",
                "url": "%s"
            }, {
                "type": "view",
                "name": "律师诉讼须知",
                "url": "%s"
            }, {
                "name": "用户导航",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "微信网站",
                        "url": "%s"
                    }, {
                        "type": "view",
                        "name": "关于我们",
                        "url": "%s"
                    }, {
                        "type": "click",
                        "name": "在线客服",
                        "key": "customer"
                    }
                ]
            }
        ]
    }"""
    print requests.post(api, menu).text
