import json
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import redirect

from users.models import Post, UserProfile, Tag, Comment, Backimage
from users.forms import LoginForm, CommentForm, RegisterForm, UserdetailForm,ResetpwdForm
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password


# Create your views here.


class IndexView(View):
    def get(self, request):
        all_posts = Post.objects.all().order_by('-add_time')

        sort = request.GET.get('lb', "")
        if sort:
            if str(sort) == 'qb':
                all_posts = Post.objects.all().order_by('-add_time')
            else:
                all_posts = all_posts.filter(tag__name=sort).order_by('-add_time')

        all_tags = Tag.objects.all()
        image = Backimage.objects.order_by('-add_time')[:1]

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_posts, 6, request=request)

        objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        all_posts = p.page(page)

        return render(request, 'blog-index.html', {
            'all_posts': all_posts,
            'all_tags': all_tags,
            'image': image,
        })


class LoginView(View):
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', "")
            pass_word = request.POST.get('password', "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request, user)
                return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')

            else:
                # return json.dumps({'status': 'fail', 'msg': "用户名或密码错误"})
                return HttpResponse(json.dumps({'status': 'fail', 'msg': "用户名或密码错误"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': "用户名或密码错误"}), content_type='application/json')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('username', "")
            password = request.POST.get('password', '')
            password2 = request.POST.get('password2', '')
            user = UserProfile.objects.filter(username=user_name)
            if user:
                return HttpResponse(json.dumps({'status': 'fail', 'msg': "用户名已经存在"}), content_type='application/json')
            elif password != password2:
                return HttpResponse(json.dumps({'status': 'fail', 'msg': "密码不一致"}), content_type='application/json')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.password = make_password(password)
            user_profile.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': "注册成功请登录"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': "注册失败"}), content_type='application/json')


class PostView(View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        all_comment = Comment.objects.filter(post=post_id).order_by('-add_time')
        image = Backimage.objects.order_by('-add_time')[:1]
        return render(request, 'post.html', {
            'post': post,
            'all_comment': all_comment,
            'image': image,
        })


class CommentView(View):
    def post(self, request):
        comment_form = CommentForm(request.POST)
        if not request.user.is_authenticated:
            return HttpResponse(json.dumps({'status': "fail", 'msg': "用户未登录"}))

        if comment_form.is_valid():
            comment = Comment()
            content = request.POST.get('content', "")
            post_id = request.POST.get('post_id', 0)
            post = Post.objects.get(id=post_id)
            comment.content = content
            comment.user = request.user
            comment.post = post
            comment.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '添加成功'}), content_type='application/json')

        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '添加失败'}), content_type='application/json')


class UserdetailView(View):
    def get(self, request):
        return render(request, 'user.html')

    def post(self, request):
        user_form = UserdetailForm(request.POST)
        if user_form.is_valid():
            address = request.POST.get('address', '')
            info = request.POST.get('info', '')
            gender = request.POST.get('gender', '')
            user = request.user
            user.address = address
            user.info = info
            user.gender = gender
            user.save()
            return redirect(reverse('user_datail',args=[]))
        else:
            return render(request, 'user.html', {'user_form': user_form})

class ResetpwdView(View):
    def post(self,request):
        resetpwd_form = ResetpwdForm(request.POST)
        if resetpwd_form.is_valid():
            password = request.POST.get('password', '')
            password2 = request.POST.get('password2', '')
            if password != password2:
                return HttpResponse(json.dumps({'status': 'fail', 'msg': '密码不一致，看样子你还是不上心啊！'}), content_type='application/json')
            user = request.user
            user.password = make_password(password)
            user.save()
            return HttpResponse(json.dumps({'status': 'success'}),content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '密码错误！'}),
                                content_type='application/json')

