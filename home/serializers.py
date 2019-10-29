#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/24 15:21
# @File    : serializers.py
# @author  : dfkai
# @Software: PyCharm
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import BlogPost, BlogCategory, BlogTag, BlogComment, BlogCollection

User = get_user_model()


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = BlogCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    # sub_cat = CategorySerializer2(many=True, read_only=True)
    sub_cat = serializers.ListField(child=RecursiveField(), read_only=True, source="sub_cat.all")
    # sub_cat = serializers.ListSerializer(child=RecursiveField(), read_only=True)

    # 反向外键引用
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=BlogPost.objects.all())

    class Meta:
        model = BlogCategory
        fields = "__all__"
        # fields = ["cate_name", "category_type", "parent_category", "create_time", "create_person", "sub_cat", "posts"]
        # list_serializer_class = CategorySerializer2


class OneCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class CommentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    user = UserSerializer(read_only=True)
    content = serializers.SerializerMethodField(read_only=True)
    sub_comment = serializers.ListField(child=RecursiveField(), read_only=True, source="sub_comment.all")

    # sub_comment = serializers.ListSerializer(child=RecursiveField(), read_only=True)

    class Meta:
        model = BlogComment
        fields = "__all__"
        # fields = ["user", "post", "nick_name", "email", "content", "create_time", "create_person"]
        # depth = 1  # 遍历深度 # 他把子项的 post 又给遍历了 ，depth越大 遍历越深
        # read_only_fields = ['user'] # 只读字段
        # extra_kwargs = {'user': {'read_only': True}} # 还有一个快捷方式，允许您使用该extra_kwargs选项在字段上指定任意其他关键字参数。与的情况一样read_only_fields，这意味着您无需在序列化程序上显式声明该字段。
        """
        这里是一些使用情况下，您可能希望定制的ListSerializer行为。例如：
        您想要提供列表的特定验证，例如检查一个元素与列表中的另一个元素没有冲突。
        您要自定义多个对象的创建或更新行为。
        对于这些情况，可以many=True通过使用list_serializer_class序列化程序Meta类上的选项来修改传递时使用的类。
        """
        # list_serializer_class = CustomListSerializer
        # 验证数据
        # validators = UniqueTogetherValidator(
        #     queryset=Event.objects.all(),
        #     fields=['room_number', 'date']
        # )

    def create(self, validated_data):
        print("two")
        comments = BlogComment.objects.create(**validated_data)  # type:BlogComment
        comments.email = "qq@qq.com"
        return comments

    def get_content(self, obj):
        if obj.is_delete:
            content = obj.content
        else:
            content = "改内容已经删除"
        return content

    # validate_ + 上面 需要验证的字段名 ，则可以自动验证 否则 将无法使用验证
    def validate_email(self, email):
        """
        验证邮箱号
        :param mobile:
        :return:
        """
        if BlogComment.objects.filter(email=email).count():
            raise serializers.ValidationError("手机号码已经存在")

        return email


class PostSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    category = OneCategorySerializer(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BlogPost
        fields = "__all__"

    def get_comments(self, obj):
        all_comments = BlogComment.objects.filter(post_id=obj.id)
        comments_serializer = CommentSerializer(all_comments,
                                                many=True, context={'request': self.context['request']})
        return comments_serializer.data


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCollection
        fields = "__all__"
