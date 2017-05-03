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
        menus[0]['menus'].append({
            'url': u'/backend/xadmin/WeWeb/userinfo/',
            'icon': 'fa fa-book',
            'order': 3,
            'perm': 'WeWeb.view_userinfo',
            'title': u'信息管理',
        })
        self.remove_origin(menus, u'信息管理')
        # 模块“小区活动”
        menus.append({
            'menus': [
                {
                    'url': u'/backend/xadmin/WeWeb/activity/',
                    'icon': 'fa fa-book',
                    'order': 1,
                    'perm': 'WeWeb.view_activity',
                    'title': u'小区活动'
                }, {
                    'url': u'/backend/xadmin/WeWeb/joinuser/',
                    'icon': 'fa fa-user',
                    'order': 2,
                    'perm': 'WeWeb.view_joinuser',
                    'title': u'报名情况'
                }],
            'first_url': u'/backend/xadmin/WeWeb/activity/',
            'title': u'小区活动',
            'first_icon': 'fa fa-lightbulb-o',
        })
        self.remove_origin(menus, u'小区活动')
        self.remove_origin(menus, u'报名情况')
        # 模块“留言板”
        menus.append({
            'menus': [
                {
                    'url': u'/backend/xadmin/WeWeb/messageboard/',
                    'icon': 'fa fa-book',
                    'order': 1,
                    'perm': 'WeWeb.view_messageboard',
                    'title': u'留言板'
                }],
            'first_url': u'/backend/xadmin/WeWeb/messageboard/',
            'title': u'留言板',
            'first_icon': 'fa fa-book'
        })
        self.remove_origin(menus, u'留言板')
        # 模块“物业缴费”
        menus.append({
            'menus': [
                {
                    'url': u'/backend/xadmin/WeWeb/payment/',
                    'icon': 'fa fa-book',
                    'order': 1,
                    'perm': 'WeWeb.view_payment',
                    'title': u'物业缴费'
                }],
            'first_url': u'/backend/xadmin/WeWeb/payment/',
            'title': u'物业缴费',
            'first_icon': 'fa fa-book'
        })
        self.remove_origin(menus, u'物业缴费')
        # 模块“场地租借”
        menus.append({
            'menus': [
                {
                    'url': u'/backend/xadmin/WeWeb/rent/',
                    'icon': 'fa fa-book',
                    'order': 1,
                    'perm': 'WeWeb.view_rent',
                    'title': u'场地租借'
                }],
            'first_url': u'/backend/xadmin/WeWeb/rent/',
            'title': u'场地租借',
            'first_icon': 'fa fa-book'
        })
        self.remove_origin(menus, u'场地租借')
        # 模块“送水上门”
        menus.append({
            'menus': [
                {
                    'url': u'/backend/xadmin/WeWeb/drink/',
                    'icon': 'fa fa-book',
                    'order': 1,
                    'perm': 'WeWeb.view_drink',
                    'title': u'饮品类型'
                }, {
                    'url': u'/backend/xadmin/WeWeb/drinkorder/',
                    'icon': 'fa fa-book',
                    'order': 2,
                    'perm': 'WeWeb.view_drinkorder',
                    'title': u'送水上门'
                }],
            'first_url': u'/backend/xadmin/WeWeb/drinkorder/',
            'title': u'送水上门',
            'first_icon': 'fa fa-book'
        })
        self.remove_origin(menus, u'饮品类型')
        self.remove_origin(menus, u'送水上门')
        return menus


class BaseSetting(object):
    """ Bind to BaseAdminView """
    enable_themes = True
    use_bootswatch = True


class RepairAdmin(object):
    pass


class ActivityAdmin(object):
    pass


class JoinUserAdmin(object):
    pass


class MessageBoardAdmin(object):
    pass


class PaymentAdmin(object):
    pass


class UserInfoAdmin(object):
    pass


class RentAdmin(object):
    pass


class DrinkAdmin(object):
    pass


class DrinkOrderAdmin(object):
    pass


xadmin.site.register(CommAdminView, GlobalSetting)
xadmin.site.register(BaseAdminView, BaseSetting)
xadmin.site.register(Repair, RepairAdmin)
xadmin.site.register(Activity, ActivityAdmin)
xadmin.site.register(JoinUser, JoinUserAdmin)
xadmin.site.register(MessageBoard, MessageBoardAdmin)
xadmin.site.register(Payment, PaymentAdmin)
xadmin.site.register(UserInfo, UserInfoAdmin)
xadmin.site.register(Rent, RepairAdmin)
xadmin.site.register(Drink, DrinkAdmin)
xadmin.site.register(DrinkOrder, DrinkOrderAdmin)
