from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    name = models.CharField(max_length=20, verbose_name="昵称")
    birday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('male', '男'), ('female', '女')), default='female')
    image = models.ImageField(upload_to='image/%Y/%m', max_length=100, default='weixin.jpg')
    comment_nums = models.IntegerField(default=0, verbose_name='评论数')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_comments(self):
        return self.comment_set.count()
