#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/6/1 11:00
@File    : urls.py
@author  : dfkai
@Software: PyCharm
"""

from django.urls import path

from . import views
from .forms import LoginForm

app_name = "users"
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path(r'users/result.html',
         views.account_result,
         name='result'),
    path('login/',
         views.LoginView.as_view(success_url='/'),
         name='login',
         kwargs={'authentication_form': LoginForm}),
    path(r'logout/',
         views.LogoutView.as_view(),
         name='logout'),
]
