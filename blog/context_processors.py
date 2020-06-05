#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.net/
@software: PyCharm
@file: context_processors.py
@time: 2016/11/6 下午4:23
"""
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def seo_processor(requests):
    value = {
        'USE_ELASTICSEARCH': settings.USE_ELASTICSEARCH,
    }
    return value
