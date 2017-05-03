# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import utc
import datetime as pdatetime
import wxtools
import config


def default_time_now():
    return datetime.utcnow().replace(tzinfo=utc)


def default_month_now():
    date_now = datetime.utcnow().replace(tzinfo=utc)
    month_now = pdatetime.date(date_now.year, date_now.month, 1)
    return month_now


class UserInfo(models.Model):
    user = models.OneToOneField(User, verbose_name='用户')
    name = models.CharField("用户名称", max_length=10, default='')
    room = models.CharField("房间号", max_length=50, default='')
    area = models.IntegerField("房屋面积", default=0)
    park = models.IntegerField("车位数", default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '信息管理'
        verbose_name_plural = verbose_name


class Repair(models.Model):
    user = models.ForeignKey(User, verbose_name="报修人")
    loc = models.CharField("故障地点", default='', max_length=50)
    desc = models.TextField("故障描述", default='')

    def __str__(self):
        return '故障地点: ' + self.loc

    class Meta:
        verbose_name = '物业报修'
        verbose_name_plural = verbose_name


class Activity(models.Model):
    name = models.CharField("活动名称", default='', max_length=50, unique=True)
    date = models.DateField("活动时间", default=default_time_now)
    detail = models.TextField("活动详情", default='')
    loc = models.CharField("活动地点", default='', max_length=50)
    member = models.IntegerField("可容纳人数", default=0)
    join = models.IntegerField("报名人数", default=0)
    rest = models.IntegerField("剩余名额", default=0)

    def save(self, *args, **kwargs):
        self.rest = self.member - self.join
        super(Activity, self).save(*args, **kwargs)

    def get_base_info(self):
        return {
            'name': self.name,
            'date': self.date.strftime('%Y-%m-%d'),
            'detail': self.detail,
            'loc': self.loc
        }

    def __str__(self):
        return '活动: ' + self.name

    class Meta:
        verbose_name = '小区活动'
        verbose_name_plural = verbose_name


class JoinUser(models.Model):
    user = models.ForeignKey(User, verbose_name="报名用户")
    activity = models.ForeignKey(Activity, verbose_name="报名活动")

    class Meta:
        verbose_name = '报名情况'
        verbose_name_plural = verbose_name
        unique_together = (('user', 'activity'),)


class MessageBoard(models.Model):
    user = models.ForeignKey(User, verbose_name="留言用户")
    message = models.TextField("留言", default='')

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = '留言板'
        verbose_name_plural = verbose_name


class Payment(models.Model):
    user = models.ForeignKey(User, verbose_name='缴费用户')
    date = models.DateField('通知日期', default=default_month_now)
    per_price = models.IntegerField('物业管理费/平', default=10)
    manage_price = models.IntegerField('物业管理费', default=0, editable=False)
    park_price = models.IntegerField('车位管理费', default=0, editable=False)
    other_price = models.IntegerField('其他费用', default=0)
    total_price = models.IntegerField('总费用', default=0, editable=False)
    paid = models.BooleanField('付费状态', default=False)

    def save(self, *args, **kwargs):
        self.manage_price = self.per_price * self.user.userinfo.area
        self.park_price = 30*self.user.userinfo.park
        self.total_price = self.manage_price + self.park_price + self.other_price
        super(Payment, self).save(*args, **kwargs)
        if self.paid:
            return
        data = {
            'touser': self.user.username,
            'template_id': 's_cQZD6stxCkmZ8e7o9Qh58-h1XtcrIhtKAL4_GM7ww',
            'url': config.authorize_uri % 'url=http://www.desckie.com/#/Pay'.replace('#', ''),
            'data': {
                'first': {
                    'value': u'本月待缴纳的物业费用',
                    'color': '#173177',
                },
                'keyword1': {
                    'value': self.user.userinfo.name,
                    'color': '#173177',
                },
                'keyword2': {
                    'value': self.user.userinfo.room,
                    'color': '#173177',
                },
                'keyword3': {
                    'value': self.total_price,
                    'color': '#173177',
                },
                'keyword4': {
                    'value': self.date.strftime('%Y年%m月'),
                    'color': '#173177',
                },
                'remark': {
                    'value': u'为保证您正常享受物业服务,请及时缴纳费用,谢谢!',
                    'color': '#173177',
                }
            }
        }
        wxtools.send_template_message(data)

    def get_pay_info(self):
        return {
            'name': self.user.userinfo.name,
            'room': self.user.userinfo.room,
            'manage_price': self.manage_price,
            'park_price': self.park_price,
            'other_price': self.other_price,
            'total_price': self.total_price
        }

    class Meta:
        verbose_name = '物业缴费'
        verbose_name_plural = verbose_name
        unique_together = (('user', 'date'),)


class Rent(models.Model):
    place = models.CharField("场地名称", max_length=50, default='')
    member = models.IntegerField("可容纳人数", default=0)
    user = models.ForeignKey(User, verbose_name='租借用户', default=None, null=True)
    rented = models.BooleanField("已租借", default=False)

    def get_place_info(self):
        return {
            'place': self.place,
            'member': self.member
        }

    def __str__(self):
        return self.place

    class Meta:
        verbose_name = '场地租借'
        verbose_name_plural = verbose_name


class Drink(models.Model):
    name = models.CharField(u"饮品名称", max_length=50, default='')
    price = models.IntegerField(u"饮品价格", default=0)

    def get_base_info(self):
        return {
            'name': self.name,
            'price': self.price
        }

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '饮品类型'
        verbose_name_plural = verbose_name


class DrinkOrder(models.Model):
    drink = models.ForeignKey(Drink, verbose_name="饮品类型")
    user = models.ForeignKey(User, verbose_name="下单用户")
    loc = models.CharField("配送地址", max_length=100, default='')
    state = models.BooleanField("已送达", default=False)

    def __str__(self):
        return self.drink.name

    class Meta:
        verbose_name = '送水上门'
        verbose_name_plural = verbose_name
