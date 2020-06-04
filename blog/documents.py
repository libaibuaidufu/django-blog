#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/6/4 9:18
@File    : documents.py
@author  : dfkai
@Software: PyCharm
"""
from django_elasticsearch_dsl import fields, Document
from django_elasticsearch_dsl.registries import registry

from blog.models import Article


@registry.register_document
class ArticleDocument(Document):
    body = fields.TextField(analyzer='ik_max_word', search_analyzer='ik_smart',
                            attr="get_body")  # 通过在 model 中定义get_body 返回内容
    title = fields.TextField(analyzer='ik_max_word', search_analyzer='ik_smart')
    author = fields.ObjectField(properties={
        'nickname': fields.TextField(analyzer='ik_max_word', search_analyzer='ik_smart'),
        'id': fields.IntegerField()
    })
    category = fields.ObjectField(properties={
        'name': fields.TextField(analyzer='ik_max_word', search_analyzer='ik_smart'),
        'id': fields.IntegerField()
    })
    tags = fields.ObjectField(properties={
        'name': fields.TextField(analyzer='ik_max_word', search_analyzer='ik_smart'),
        'id': fields.IntegerField()
    })

    # pub_time = fields.Date()
    # status = fields.Text()
    # comment_status = fields.Text()
    # type = fields.Text()
    # views = fields.Integer()
    # article_order = fields.Integer()

    class Index:
        name = 'blog'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Article  # The model associated with this Document

        fields = [
            "pub_time",
            "status",
            "comment_status",
            "type",
            "views",
            "article_order",
        ]  # 上面重新定义了 这里就不用定义了
