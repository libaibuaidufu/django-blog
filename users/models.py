# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


# Create your models here.

class UserProfile(AbstractUser):
    nickname = models.CharField('昵称', max_length=100, blank=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)
    source = models.CharField("创建来源", max_length=100, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-id']
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    def get_absolute_url(self):
        return reverse(
            'blog:author_detail', kwargs={
                'author_name': self.username})
