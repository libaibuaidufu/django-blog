# coding:utf-8
__author__ = "dfk"
__date__ = "2017/12/25 10:14"
from django import forms

from users.models import Comment, UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class ResetpwdForm(forms.Form):
    password = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UserdetailForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['address', 'info', 'gender']
