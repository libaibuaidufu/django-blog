from django.db.models.signals import post_save,pre_save,m2m_changed
from django.dispatch import receiver
from .models import Post,Tag


@receiver(m2m_changed,sender=Post.tag.through)
def post_click(sender,instance=None,reverse=False,action=None,**kwargs):
    if action=='post_add':
        # post = Post.objects.get(id=instance.id)
        all_tags = instance.tag.all()
        for tag in all_tags:
            tag.tag_nums += 1
            tag.save()


# def post_nums(sender,instance,**kwargs):
#     post_id = instance.id
#     post = Post.objects.get(id=post_id)
#     all_tags = post.tag.all()
#     print('xx')
#     for tag in all_tags:
#         tag.tag_nums+=1
#         tag.save()
#
# m2m_changed.connect(post_nums,sender=Post.tag.through)