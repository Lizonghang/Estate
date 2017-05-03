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
        # 模块“用户管理”
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
        # 模块“物业报修”
        menus[1]['menus'][0]['icon'] = 'fa fa-phone'
        # 模块“小区活动”
        menus.append({
            'menus': [
                {
                    'url': u'/backend/xadmin/WeWeb/activity/',
                    'icon': 'fa fa-users',
                    'order': 1,
                    'perm': 'WeWeb.view_activity',
                    'title': u'小区活动'
                }, {
                    'url': u'/backend/xadmin/WeWeb/joinuser/',
                    'icon': 'fa fa-sign-in',
                    'order': 2,
                    'perm': 'WeWeb.view_joinuser',
                    'title': u'报名情况'
                }],
            'first_url': u'/backend/xadmin/WeWeb/activity/',
            'title': u'小区活动',
            'first_icon': 'fa fa-users',
        })
        self.remove_origin(menus, u'小区活动')
        self.remove_origin(menus, u'报名情况')
        # 模块“留言板”
        menus.append({
            'menus': [
                {
                    'url': u'/backend/xadmin/WeWeb/messageboard/',
                    'icon': 'fa fa-clipboard',
                    'order': 1,
                    'perm': 'WeWeb.view_messageboard',
                    'title': u'留言板'
                }],
            'first_url': u'/backend/xadmin/WeWeb/messageboard/',
            'title': u'留言板',
            'first_icon': 'fa clipboard'
        })
        self.remove_origin(menus, u'留言板')
        # 模块“物业缴费”
        menus.append({
            'menus': [
                {
                    'url': u'/backend/xadmin/WeWeb/payment/',
                    'icon': 'fa fa-money',
                    'order': 1,
                    'perm': 'WeWeb.view_payment',
                    'title': u'物业缴费'
                }],
            'first_url': u'/backend/xadmin/WeWeb/payment/',
            'title': u'物业缴费',
            'first_icon': 'fa fa-money'
        })
        self.remove_origin(menus, u'物业缴费')
        # 模块“场地租借”
        menus.append({
            'menus': [
                {
                    'url': u'/backend/xadmin/WeWeb/rent/',
                    'icon': 'fa fa-table',
                    'order': 1,
                    'perm': 'WeWeb.view_rent',
                    'title': u'场地租借'
                }],
            'first_url': u'/backend/xadmin/WeWeb/rent/',
            'title': u'场地租借',
            'first_icon': 'fa fa-table'
        })
        self.remove_origin(menus, u'场地租借')
        # 模块“送水上门”
        menus.append({
            'menus': [
                {
                    'url': u'/backend/xadmin/WeWeb/drink/',
                    'icon': 'fa fa-coffee',
                    'order': 1,
                    'perm': 'WeWeb.view_drink',
                    'title': u'饮品类型'
                }, {
                    'url': u'/backend/xadmin/WeWeb/drinkorder/',
                    'icon': 'fa fa-flash',
                    'order': 2,
                    'perm': 'WeWeb.view_drinkorder',
                    'title': u'送水上门'
                }],
            'first_url': u'/backend/xadmin/WeWeb/drinkorder/',
            'title': u'送水上门',
            'first_icon': 'fa fa-coffee'
        })
        self.remove_origin(menus, u'饮品类型')
        self.remove_origin(menus, u'送水上门')
        # 模块“失物招领”
        menus.append({
            'menus': [
                {
                    'url': u'/backend/xadmin/WeWeb/loseandfound/',
                    'icon': 'fa fa-suitcase',
                    'order': 1,
                    'perm': 'WeWeb.view_loseandfound',
                    'title': u'失物招领'
                }],
            'first_url': u'/backend/xadmin/WeWeb/loseandfound/',
            'title': u'失物招领',
            'first_icon': 'fa fa-suitcase'
        })
        self.remove_origin(menus, u'失物招领')
        # 模块“其他设置”
        menus.append({
            'menus': [
                {
                    'url': u'/backend/xadmin/WeWeb/banner/',
                    'icon': 'fa fa-picture-o',
                    'order': 1,
                    'perm': 'WeWeb.view_banner',
                    'title': u'轮播图'
                }],
            'first_url': u'/backend/xadmin/WeWeb/banner/',
            'title': u'其他设置',
            'first_icon': 'fa fa-cog'
        })
        self.remove_origin(menus, u'轮播图')
        return menus


class BaseSetting(object):
    """ Bind to BaseAdminView """
    enable_themes = True
    use_bootswatch = True


class RepairAdmin(object):
    list_display = ('loc', 'desc', 'user__userinfo__name', 'state')
    list_editable = ('state',)
    list_filter = ('state',)


class ActivityAdmin(object):
    list_display = ('name', 'loc', 'date', 'member', 'join', 'rest')
    exclude = ('join', 'rest')


class JoinUserAdmin(object):
    list_display = ('user__userinfo__name', 'activity__name')
    list_filter = ('activity__name',)


class MessageBoardAdmin(object):
    list_display = ('user__userinfo__name', 'message')


class PaymentAdmin(object):
    list_display = ('user__userinfo__name', 'manage_price', 'park_price', 'other_price', 'total_price', 'date', 'paid')
    exclude = ('paid',)
    list_editable = ('paid',)
    list_filter = ('user__userinfo__name', 'date', 'paid')


class UserInfoAdmin(object):
    list_display = ('user', 'name', 'room', 'area', 'park')
    list_editable = ('name', 'room', 'area', 'park')
    list_filter = ('user', 'name', 'room')


class RentAdmin(object):
    list_display = ('place', 'member', 'user', 'rented')
    list_editable = ('user', 'rented')
    list_filter = ('place', 'rented')


class DrinkAdmin(object):
    list_display = ('name', 'price')
    list_editable = ('name', 'price')
    list_filter = ('name',)


class DrinkOrderAdmin(object):
    list_display = ('user__userinfo__name', 'drink', 'loc', 'state')
    exclude = ('state',)
    list_editable = ('state',)
    list_filter = ('drink', 'state')


class LoseAndFoundAdmin(object):
    list_display = ('name', 'desc', 'date', 'state')
    exclude = ('state',)
    list_editable = ('name', 'desc', 'state')
    list_filter = ('name', 'state')


class BannerAdmin(object):
    list_display = ('image',)


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
xadmin.site.register(LoseAndFound, LoseAndFoundAdmin)
xadmin.site.register(Banner, BannerAdmin)
