# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist
from WeWeb.models import *
import time
import re


class VisitorHandler:

    def __init__(self, XMLdata):
        self.XMLdata = XMLdata

    def get_message(self):
        fromUser, toUser = self._parse(self.XMLdata)
        user = User.objects.get(username=fromUser)
        try:
            user.userinfo
        except ObjectDoesNotExist:
            return self._get_fail_response(fromUser, toUser)
        Visitor.objects.create(master=user)
        return self._get_success_response(fromUser, toUser)

    def _parse(self, XMLdata):
        fromUser = XMLdata.find('FromUserName').get_text()
        toUser = XMLdata.find('ToUserName').get_text()
        return fromUser, toUser

    def _get_success_response(self, fromUser, toUser):
        create_time = int(time.time())
        ret_xml = """
        <xml>
         <ToUserName><![CDATA[""" + fromUser + """]]></ToUserName>
         <FromUserName><![CDATA[""" + toUser + """]]></FromUserName>
         <CreateTime>""" + str(create_time) + """</CreateTime>
         <MsgType><![CDATA[text]]></MsgType>
         <Content><![CDATA[请输入来访客人姓名,如<a href="#">#张三#</a>。若有多人来访,仅填写一人姓名即可。]]></Content>
        </xml> """
        return ret_xml

    def _get_fail_response(self, fromUser, toUser):
        create_time = int(time.time())
        bind = config.authorize_uri % 'url=http://www.desckie.com/#/'.replace('#', '')
        ret_xml = """
        <xml>
         <ToUserName><![CDATA[""" + fromUser + """]]></ToUserName>
         <FromUserName><![CDATA[""" + toUser + """]]></FromUserName>
         <CreateTime>""" + str(create_time) + """</CreateTime>
         <MsgType><![CDATA[text]]></MsgType>
         <Content><![CDATA[您尚未进行住户信息绑定,无法进行该操作。请先进行<a href="{0}">住户绑定</a>]]></Content>
        </xml> """.format(bind)
        return ret_xml


class VisitorBindHandler:

    def __init__(self, XMLdata):
        self.XMLdata = XMLdata

    def get_message(self):
        fromUser, toUser, Content = self._parse(self.XMLdata)
        matches = re.findall(r'#(.*?)#', Content)
        if len(matches) != 1:
            return self._get_fail_response(fromUser, toUser, 1)
        user = User.objects.get(username=fromUser)
        try:
            visitor = Visitor.objects.get(master=user)
        except ObjectDoesNotExist:
            return self._get_fail_response(fromUser, toUser, 2)
        return self._get_success_response(fromUser, toUser, visitor)

    def _parse(self, XMLdata):
        fromUser = XMLdata.find('FromUserName').get_text()
        toUser = XMLdata.find('ToUserName').get_text()
        Content = XMLdata.find('Content').get_text().strip()
        return fromUser, toUser, Content

    def _get_success_response(self, fromUser, toUser, visitor):
        msg = '预约来访客人姓名: <a href="#">{0}</a>, 预约码: <a href="#">{1}</a>。来访客人进入小区时请出示该预约码与个人证件,感谢您的预约!'.format(visitor.visitor, visitor.code)
        create_time = int(time.time())
        ret_xml = """
        <xml>
         <ToUserName><![CDATA[""" + fromUser + """]]></ToUserName>
         <FromUserName><![CDATA[""" + toUser + """]]></FromUserName>
         <CreateTime>""" + str(create_time) + """</CreateTime>
         <MsgType><![CDATA[text]]></MsgType>
         <Content><![CDATA[""" + msg + """]]></Content>
        </xml> """
        return ret_xml

    def _get_fail_response(self, fromUser, toUser, errcode):
        if errcode == 1:
            errmsg = '请将来访客人姓名使用双#号括起,如<a href="#">#张三#</a>。若有多人一起来访,仅填写其中一人姓名即可。'
        elif errcode == 2:
            errmsg = '请先通过"快捷服务->访客预约"创建预约记录'
        else:
            errmsg = '未知错误'
        create_time = int(time.time())
        ret_xml = """
        <xml>
         <ToUserName><![CDATA[""" + fromUser + """]]></ToUserName>
         <FromUserName><![CDATA[""" + toUser + """]]></FromUserName>
         <CreateTime>""" + str(create_time) + """</CreateTime>
         <MsgType><![CDATA[text]]></MsgType>
         <Content><![CDATA[""" + errmsg + """]]></Content>
        </xml> """
        return ret_xml
