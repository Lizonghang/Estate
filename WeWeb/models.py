# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class Test(models.Model):
    text = models.TextField("测试")

    class Meta:
        verbose_name = u'测试'
        verbose_name_plural = u'测试'
