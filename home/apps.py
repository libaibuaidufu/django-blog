from django.apps import AppConfig


class HomeConfig(AppConfig):
    name = 'home'
    verbose_name = "用户管理"

    def ready(self):
        import home.singals