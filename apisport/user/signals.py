from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserInfo, User


@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user_id=instance)
        print("UserInfo created for user:", instance.username)
