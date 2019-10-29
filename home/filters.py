#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/24 17:34
# @File    : filters.py
# @author  : dfkai
# @Software: PyCharm
import django_filters
from django.db.models import Q

from .models import BlogPost


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品的过滤类
    """
    # gte 大于等于  lte小于等于
    # pricemin = django_filters.NumberFilter(name="shop_price", lookup_expr='gte')
    # pricemax = django_filters.NumberFilter(name="shop_price", lookup_expr='lte')
    # name = filters.CharFilter(name='name', lookup_expr='icontains')
    top_category = django_filters.NumberFilter(method='top_category_filter')

    # 假如传递过来的是一级类目 就是第一个  id 等于传递过来的value
    def top_category_filter(self, queryset, name, value):
        # return queryset.filter(category_id=value)
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = BlogPost
        # fields = "__all__"  # ['pricemin', 'pricemax', 'top_category', 'is_hot', 'is_new']
        fields = ["top_category", 'is_hot', 'is_new']  # ['pricemin', 'pricemax', 'top_category']
