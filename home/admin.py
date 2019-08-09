from django.contrib import admin
from django.db.models import ManyToOneRel, ForeignKey, OneToOneField, ManyToManyField
from .models import BlogCategory, BlogCollection, BlogComment, BlogPost, BlogTag


# Register your models here.
class CustomModelAdminMixin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.get_fields() if field.name != "uid"]
        super(CustomModelAdminMixin, self).__init__(model, admin_site)


class BlogCategoryAdmin(admin.ModelAdmin):
    model = BlogCategory
    list_display = [field.name for field in model._meta.get_fields() if
                    not isinstance(field, (ManyToOneRel, ForeignKey, OneToOneField, ManyToManyField))]
    # pass


class BlogCollectionAdmin(CustomModelAdminMixin):
    # model = BlogCollection
    pass


class BlogCommentAdmin(CustomModelAdminMixin):
    # model = BlogComment
    pass


class BlogPostAdmin(admin.ModelAdmin):
    model = BlogPost
    list_display = [field.name for field in model._meta.get_fields() if
                    not isinstance(field, (ManyToOneRel, ForeignKey, OneToOneField, ManyToManyField))]
    # pass


class BlogTagAdmin(CustomModelAdminMixin):
    # model = BlogTag
    pass


admin.site.register(BlogCollection, BlogCollectionAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)
admin.site.register(BlogTag, BlogTagAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
