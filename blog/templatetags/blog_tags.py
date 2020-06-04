#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/5/29 11:45
@File    : blog_tags.py
@author  : dfkai
@Software: PyCharm
"""
import hashlib
import logging
import urllib.request as urllib2

from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from blog.models import Category

logger = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def datetimeformat(data):
    try:
        return data.strftime(settings.DATE_TIME_FORMAT)
    except Exception as e:
        logger.error(e)
        return ""


@register.simple_tag
def query_category(parent_category):
    """
    获得分类
    :return:
    """
    nav_category = Category.objects.filter(parent_category=parent_category).all()
    return nav_category


@register.filter(is_safe=True)
@stringfilter
def custom_markdown(content):
    from blog_co.utils import CommonMarkdown
    return mark_safe(CommonMarkdown.get_markdown(content))


@register.simple_tag
def query(qs, **kwargs):
    """ template tag which allows queryset filtering. Usage:
          {% query books author=author as mybooks %}
          {% for book in mybooks %}
            ...
          {% endfor %}
    """
    return qs.filter(**kwargs)


@register.simple_tag
def gravatar_url(email, size=50, verify_default=False):
    """Construct the gravatar url."""
    gravatar_url = ''.join(['http://www.gravatar.com/avatar/',
                            hashlib.md5(email.lower().encode("utf-8")).hexdigest(), '?s=%d' % size])
    # if default return None
    if (verify_default):
        gravatar_url += '&d=404'
        try:
            urllib2.urlopen(gravatar_url)
        except urllib2.URLError as  e:
            return None
    return gravatar_url
