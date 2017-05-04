# coding=utf-8
from WeWeb.models import *
import time


class VisitorHandler:

    def __init__(self, XMLdata):
        self.XMLdata = XMLdata

    def get_message(self):
        fromUser, toUser = self._parse(self.XMLdata)
        user = User.objects.get(username=fromUser)
        Visitor.objects.create(master=user)
        ret_xml = self._get_subscribe_response(fromUser, toUser)
        return ret_xml

    def _parse(self, XMLdata):
        fromUser = XMLdata.find('FromUserName').get_text()
        toUser = XMLdata.find('ToUserName').get_text()
        return fromUser, toUser

    def _get_subscribe_response(self, fromUser, toUser):
        create_time = int(time.time())
        ret_xml = """
        <xml>
         <ToUserName><![CDATA[""" + fromUser + """]]></ToUserName>
         <FromUserName><![CDATA[""" + toUser + """]]></FromUserName>
         <CreateTime>""" + str(create_time) + """</CreateTime>
         <MsgType><![CDATA[text]]></MsgType>
         <Content><![CDATA[请输入来访客人姓名]]></Content>
        </xml> """
        return ret_xml
