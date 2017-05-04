from WXEventHandler.Subscribe import SubscribeHandler
from WXEventHandler.Vistor import VisitorHandler, VisitorBindHandler
from bs4 import BeautifulSoup
import config


class WXMsgHandler:
    def __init__(self, request, token, params):
        self.token = token
        self.params = params
        self.wxAppID = config.wxAppID
        self.xml = request.body

    def event_router(self):
        XMLdata = BeautifulSoup(self.xml, "lxml-xml")
        MsgType = XMLdata.find('MsgType').get_text()
        if MsgType == 'event':
            Event = XMLdata.find('Event').get_text()
            if Event == 'subscribe':
                handler = SubscribeHandler(XMLdata)
                return handler.get_message()
            if Event == 'CLICK':
                EventKey = XMLdata.find('EventKey').get_text()
                if EventKey == 'fangkeyuyue':
                    handler = VisitorHandler(XMLdata)
                    return handler.get_message()
        elif MsgType == 'text':
            Content = XMLdata.find('Content').get_text().strip()
            if '#' in Content:
                handler = VisitorBindHandler(XMLdata)
                return handler.get_message()
        return ''
