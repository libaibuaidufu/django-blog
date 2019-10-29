#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/27 16:15
# @File    : test.py
# @author  : dfkai
# @Software: PyCharm

import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from home.models import BlogCollection

cs = BlogCollection.objects.filter(post_id=1)
cs.update(user_id=2)
