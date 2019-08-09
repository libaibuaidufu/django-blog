import json

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.views import View

from .forms import LoginForm, RegisterForm
from .models import UserProfile


# Create your views here.
# 自定义验证
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse(json.dumps({'status': 'fail', 'msg': '密码或者用户名错误'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'login_form': login_form.errors}), content_type='application/json')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):

    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        register_forms = RegisterForm(request.POST)
        if register_forms.is_valid():
            username = request.POST.get("username", '')
            if UserProfile.objects.filter(username=username):
                return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户名已存在'}))
            password = request.POST.get("password", "")
            user = UserProfile()
            user.username = username
            user.name = username
            user.password = make_password(password)
            user.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse(json.dumps({"status": 'fail', 'register_form': register_forms.errors}))
