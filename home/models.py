# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from datetime import datetime

import markdown
# from DjangoUeditor.models import UEditorField
from ckeditor.fields import RichTextField
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from users.models import UserProfile
from mdeditor.fields import MDTextField


class BlogCategory(models.Model):
    cate_pid = models.IntegerField(blank=True, null=True)
    cate_name = models.CharField(max_length=30, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    create_person = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = u"分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.cate_name

    def get_post_num(self):
        return self.blogpost_set.count()

    def get_all_post(self):
        return self.blogpost_set.all()


class BlogCollection(models.Model):
    post_id = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        # db_table = 'blog_collection'
        verbose_name = u"收藏"
        verbose_name_plural = verbose_name


class BlogTag(models.Model):
    tag_name = models.CharField(max_length=30, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    create_person = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        # db_table = 'blog_tag'
        verbose_name = u"标签"
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.tag_name


class BlogPost(models.Model):
    category = models.ForeignKey(BlogCategory, verbose_name="类别", on_delete=models.DO_NOTHING)
    tag = models.ManyToManyField(BlogTag, verbose_name="标签", null=True, blank=True, related_name='tags')
    name = models.CharField(max_length=50, verbose_name='文章名')
    author = models.ForeignKey(UserProfile, verbose_name="作者", on_delete=models.DO_NOTHING)
    # content = UEditorField(verbose_name='文章内容', width=600, height=300, imagePath="post/ueditor/",
    #                        filePath="post/ueditor/",
    #                        default='')
    # content = RichTextUploadingField()
    content = MDTextField()
    is_hot = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    click_nums = models.IntegerField(default=0, null=True, blank=True)
    fav_nums = models.IntegerField(default=0, null=True, blank=True)

    add_time = models.DateField(default=datetime.now)

    class Meta:
        db_table = 'blog_post'
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_comment_all(self):
        comment_list = self.blogcomment_set.order_by("-create_time").all()
        for comment in comment_list:
            comment.md_content = comment.content
            comment.content = markdown.markdown(comment.content,
                                                extensions=[
                                                    'markdown.extensions.extra',
                                                    'markdown.extensions.codehilite',
                                                    'markdown.extensions.toc',
                                                ], safe_mode=True, enable_attributes=False)
        return comment_list


class BlogComment(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.DO_NOTHING, blank=True, null=True)
    post = models.ForeignKey(BlogPost, verbose_name="文章", on_delete=models.DO_NOTHING)
    nick_name = models.CharField(max_length=30, verbose_name="留言用户名", default="admin")
    email = models.EmailField(max_length=30, verbose_name="邮箱", default="admin@admin.com")
    content = MDTextField(blank=True, null=True)  # models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True, default=datetime.now)
    create_person = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # db_table = 'blog_comment'
        verbose_name = u"评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class SsrModel(models.Model):
    path = models.CharField(max_length=255, verbose_name="名称")
    create_time = models.DateTimeField(default=datetime.utcnow)

    class Meta:
        verbose_name = "酸酸乳"
        verbose_name_plural = verbose_name
