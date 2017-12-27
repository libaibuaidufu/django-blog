# coding:utf-8
from datetime import datetime
from DjangoUeditor.models import UEditorField

from django.db import models
from django.contrib.auth.models import AbstractUser
from DjangoUeditor.models import UEditorField


# Create your models here.

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称')
    gender = models.CharField(max_length=6, choices=(('male', '男'), ('female', "女")), default='male',verbose_name='性别')
    address = models.CharField(max_length=100, default='',verbose_name='地址')
    info = models.CharField(max_length=300,verbose_name='介绍',default='')
    image = models.ImageField(upload_to='image/%Y/%m', default='', verbose_name='头像')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='类名')
    add_time = models.DateTimeField(verbose_name='时间', default=datetime.now)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    tag = models.ForeignKey(Tag, verbose_name='标签')
    name = models.CharField(max_length=30, verbose_name='文章名')
    content = UEditorField(verbose_name='文章内容', width=600, height=300, imagePath="post/ueditor/",
                           filePath="post/ueditor/",
                           default='')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    add_time = models.DateTimeField(verbose_name='发表时间', default=datetime.now)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Comment(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    post = models.ForeignKey(Post,verbose_name='文章',null=True,blank=True)
    content = UEditorField(u'评论', width=600, height=300, toolbars="mini")
    add_time = models.DateTimeField(verbose_name='时间', default=datetime.now)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user__name

class Backimage(models.Model):
    name = models.CharField(max_length=30, verbose_name='图名')
    image = models.ImageField(upload_to='iamge/%Y/%m',verbose_name="背景图")
    add_time = models.DateTimeField(verbose_name='时间', default=datetime.now)

    class Meta:
        verbose_name = '背景图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
