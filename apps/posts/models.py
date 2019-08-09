from datetime import datetime
from django.db import models
from tinymce.models import HTMLField

from DjangoUeditor.models import UEditorField
from users.models import UserProfile


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=10, verbose_name='类别')

    add_time = models.DateField(default=datetime.now)

    class Meta:
        verbose_name = "类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=20,verbose_name='标签')
    tag_nums = models.IntegerField(default=0,verbose_name='标签文章')

    add_time = models.DateField(default=datetime.now)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(Category, verbose_name="类别")
    tag = models.ManyToManyField(Tag,verbose_name="标签",null=True,blank=True,related_name='tags')
    name = models.CharField(max_length=50, verbose_name='文章名')
    author = models.ForeignKey(UserProfile, verbose_name="作者")
    content =  UEditorField(verbose_name='文章内容', width=600, height=300, imagePath="post/ueditor/",
                           filePath="post/ueditor/",
                           default='')
    is_hot = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    click_nums = models.IntegerField(default=0,null=True,blank=True)
    fav_nums =models.IntegerField(default=0,null=True,blank=True)


    add_time = models.DateField(default=datetime.now)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_comments(self):
        return self.comment_set.all()




class Comment(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name="用户")
    post = models.ForeignKey(Post,verbose_name="文章",null=True,blank=True)
    content = models.TextField()
    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class TodayOne(models.Model):
    name = models.CharField(max_length=20, verbose_name='每日一句')
    content = models.CharField(max_length=300, verbose_name='内容')

    add_time = models.DateField(default=datetime.now)

    class Meta:
        verbose_name = "每日一句"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tell(models.Model):
    name = models.CharField(max_length=20, verbose_name='网站公告')
    content = models.CharField(max_length=300, verbose_name='公告')

    add_time = models.DateField(default=datetime.now)

    class Meta:
        verbose_name = "网站公告"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class IndexAD(models.Model):
    name = models.CharField(max_length=30, verbose_name='广告')
    image = models.ImageField(upload_to='index/%Y/%m', max_length=200, verbose_name='图片')

    add_time = models.DateField(default=datetime.now)

    class Meta:
        verbose_name = "网站广告"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


