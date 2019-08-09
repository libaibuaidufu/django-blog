#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class UserProfile(AbstractUser):
    # user_name = models.CharField(max_length=20, blank=True, null=True)
    nick_name = models.CharField(max_length=20, blank=True, null=True)
    # password = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    birthdate = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    # email = models.CharField(max_length=40, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    reg_ip = models.CharField(max_length=255, blank=True, null=True)
    reg_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
