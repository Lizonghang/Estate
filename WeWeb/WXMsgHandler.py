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
        return ''
