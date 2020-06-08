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
from datetime import datetime

from django.conf import settings

logger = logging.getLogger(__name__)


def seo_processor(requests):
    class blog_co_setting():
        sitename = "随风潜入夜",
        show_google_adsense = False,
        google_adsense_codes = "谷歌广告代码",
        site_seo_description = "网站seo描述",
        site_description = "网站描述",
        site_keywords = "网站关键词",
        article_sub_length = "文章摘要长度",
        nav_category_list = [],
        nav_pages = "",
        open_site_comment = True,  # 是否开启评论
        beiancode = "备案代码",
        analyticscode = "网站统计代码",
        gongan_beiancode = "公安备案号",
        show_gongan_code = True,
        current_year = datetime.now().year

    value = {
        'USE_ELASTICSEARCH': settings.USE_ELASTICSEARCH,
        'SITE_NAME': blog_co_setting.sitename,
        'SHOW_GOOGLE_ADSENSE': blog_co_setting.show_google_adsense,
        'GOOGLE_ADSENSE_CODES': blog_co_setting.google_adsense_codes,
        'SITE_SEO_DESCRIPTION': blog_co_setting.site_seo_description,
        'SITE_DESCRIPTION': blog_co_setting.site_description,
        'SITE_KEYWORDS': blog_co_setting.site_keywords,
        'SITE_BASE_URL': requests.scheme + '://' + requests.get_host() + '/',
        'ARTICLE_SUB_LENGTH': blog_co_setting.article_sub_length,
        'nav_category_list': blog_co_setting.nav_category_list,  # Category.objects.all(),
        'nav_pages': blog_co_setting.nav_pages,
        'OPEN_SITE_COMMENT': blog_co_setting.open_site_comment,
        'BEIAN_CODE': blog_co_setting.beiancode,
        'ANALYTICS_CODE': blog_co_setting.analyticscode,
        "BEIAN_CODE_GONGAN": blog_co_setting.gongan_beiancode,
        "SHOW_GONGAN_CODE": blog_co_setting.show_gongan_code,
        "CURRENT_YEAR": datetime.now().year}
    return value
