# encoding: utf-8
from xadmin.views import CommAdminView, BaseAdminView
from .models import *
import xadmin


class GlobalSetting(object):
    """ Bind to CommAdminView """
    site_title = u"UESTC物业管理页面"
    site_footer = u"程彦衡支持开发"
    apps_label_title = {
        'auth': u'用户管理',
        'weweb': u'物业报修',
    }

    def remove_origin(self, menus, dbtable):
        """ remove dbtable from origin menu """
        item = [item for item in menus[1]['menus'] if item['title'] == dbtable]
        if item:
            menus[1]['menus'].remove(item.pop())

    def get_nav_menu(self):
        menus = super(GlobalSetting, self).get_nav_menu()
        # 确认AUTH栏和WEWEB栏顺序
        if menus[0]['title'] != u'用户管理':
            temp = menus[0]
            menus[0] = menus[1]
            menus[1] = temp
            del temp
            # 删除AUTH栏“组”与“权限”
        del menus[0]['menus'][2]
        del menus[0]['menus'][0]
        return menus


class BaseSetting(object):
    """ Bind to BaseAdminView """
    enable_themes = True
    use_bootswatch = True


class RepairAdmin(object):
    pass


xadmin.site.register(CommAdminView, GlobalSetting)
xadmin.site.register(BaseAdminView, BaseSetting)
xadmin.site.register(Repair, RepairAdmin)
