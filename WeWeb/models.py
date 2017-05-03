# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import utc


def default_time_now():
    return datetime.utcnow().replace(tzinfo=utc)


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
