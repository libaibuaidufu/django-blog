#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/28 9:29
# @File    : singals.py
# @author  : dfkai
# @Software: PyCharm
from django.contrib.auth.views import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        print("in")
        password = instance.password
        instance.set_password(password)
        instance.save()
        # Token.objects.create(user=instance)
    print("out")
