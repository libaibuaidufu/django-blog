#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/8 10:42
# @Site    : 
# @File    : froms.py
# @Software: PyCharm

from django import forms

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'password']
