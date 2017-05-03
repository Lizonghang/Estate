# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class Repair(models.Model):
    user = models.ForeignKey(User, verbose_name="报修人")
    loc = models.CharField("故障地点", default='', max_length=50)
    desc = models.TextField("故障描述", default='')

    class Meta:
        verbose_name = '物业报修'
        verbose_name_plural = verbose_name
