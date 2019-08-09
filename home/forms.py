#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/8 22:32
# @Site    : 
# @File    : forms.py
# @Software: PyCharm
from django import forms


class FileForms(forms.Form):
    path = forms.CharField(required=True, max_length=255)
