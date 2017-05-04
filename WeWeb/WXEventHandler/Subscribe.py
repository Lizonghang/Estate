# encoding: utf-8
import time
from WeWeb import config
from django.contrib.auth.models import User


class SubscribeHandler:

    def __init__(self, XMLdata):
        self.XMLdata = XMLdata

    def get_message(self):
        fromUser, toUser = self._parse(self.XMLdata)
        User.objects.get_or_create(username=fromUser)
        return self._get_subscribe_response(fromUser, toUser)

    def _parse(self, XMLdata):
        fromUser = XMLdata.find('FromUserName').get_text()
        toUser = XMLdata.find('ToUserName').get_text()
        return fromUser, toUser

    def _get_subscribe_response(self, fromUser, toUser):
        create_time = int(time.time())
        bind = config.authorize_uri % 'url=http://www.desckie.com/#/'.replace('#', '')
        ret_xml = """
        <xml>
         <ToUserName><![CDATA[""" + fromUser + """]]></ToUserName>
         <FromUserName><![CDATA[""" + toUser + """]]></FromUserName>
         <CreateTime>""" + str(create_time) + """</CreateTime>
         <MsgType><![CDATA[text]]></MsgType>
         <Content><![CDATA[欢迎关注UESTC物业管理平台,请点击进行<a href="{0}">住户绑定</a>]]></Content>
        </xml> """.format(bind)
        return ret_xml
