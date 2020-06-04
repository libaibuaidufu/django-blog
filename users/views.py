import logging

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView

from blog_co.utils import get_md5, send_email
from .forms import RegisterForm, LoginForm
from .models import UserProfile

logger = logging.getLogger(__name__)

# Create your views here.
User: UserProfile = get_user_model()


# 这种写法很像 drf 中的写法
class LoginView(FormView):
    form_class = LoginForm  # 这个就像是 seriarlizer_class 估计也有 get_form_class 这个函数
    template_name = 'users/login.html'  # 指定模板
    success_url = '/'  # 成功后 跳转地址
    redirect_field_name = REDIRECT_FIELD_NAME  # 覆盖next是否GET传递给定 参数。

    @method_decorator(sensitive_post_parameters('password'))  # 屏蔽敏感字段
    @method_decorator(csrf_protect)  # 跨域保护
    @method_decorator(never_cache)  # 不做缓存
    def dispatch(self, request, *args, **kwargs):

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):  # 添加 参数到模板
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if redirect_to is None:
            redirect_to = '/'
        kwargs['redirect_to'] = redirect_to

        return super(LoginView, self).get_context_data(**kwargs)

    def form_valid(self, form):  # 验证表单
        form = AuthenticationForm(data=self.request.POST, request=self.request)

        if form.is_valid():
            logger.info(self.redirect_field_name)

            auth.login(self.request, form.get_user())
            return super(LoginView, self).form_valid(form)
            # return HttpResponseRedirect('/')
        else:
            return self.render_to_response({
                'form': form
            })

    def get_success_url(self):  # 获取跳转后的地址
        # 检测地址是否安全
        redirect_to = self.request.POST.get(self.redirect_field_name)
        if not is_safe_url(
                url=redirect_to, allowed_hosts=[
                    self.request.get_host()]):
            redirect_to = self.success_url
        return redirect_to


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "users/register.html"

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(False)  # False 先不做提交
            user.is_active = False
            user.source = 'Register'
            user.save(True)  # 再提交
            site = settings.SITE
            sign = get_md5(get_md5(settings.SECRET_KEY + str(user.id)))

            if settings.DEBUG:
                site = '127.0.0.1:8000'
            path = reverse('users:result')
            url = "http://{site}{path}?type=validation&id={id}&sign={sign}".format(
                site=site, path=path, id=user.id, sign=sign)

            content = """
                            <p>请点击下面链接验证您的邮箱</p>

                            <a href="{url}" rel="bookmark">{url}</a>

                            再次感谢您！
                            <br />
                            如果上面链接无法打开，请将此链接复制至浏览器。
                            {url}
                            """.format(url=url)
            send_email(
                emailto=[
                    user.email,
                ],
                title='验证您的电子邮箱',
                content=content)

            url = reverse('users:result') + \
                  '?type=register&id=' + str(user.id)
            return HttpResponseRedirect(url)  # 重定向url
        else:
            return self.render_to_response({
                'form': form
            })


class LogoutView(RedirectView):
    url = '/login/'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


def account_result(request):
    type = request.GET.get('type')
    id = request.GET.get('id')

    user = get_object_or_404(get_user_model(), id=id)  # get_object_or_404 快捷查询 model
    logger.info(type)
    if user.is_active:
        return HttpResponseRedirect('/')
    if type and type in ['register', 'validation']:
        if type == 'register':
            content = '''
    恭喜您注册成功，一封验证邮件已经发送到您 {email} 的邮箱，请验证您的邮箱后登录本站。
    '''.format(email=user.email)
            title = '注册成功'
        else:
            c_sign = get_md5(get_md5(settings.SECRET_KEY + str(user.id)))
            sign = request.GET.get('sign')
            if sign != c_sign:
                return HttpResponseForbidden()
            user.is_active = True
            user.save()
            content = '''
            恭喜您已经成功的完成邮箱验证，您现在可以使用您的账号来登录本站。
            '''
            title = '验证成功'
        return render(request, 'users/result.html', {
            'title': title,
            'content': content
        })
    else:
        return HttpResponseRedirect('/')
