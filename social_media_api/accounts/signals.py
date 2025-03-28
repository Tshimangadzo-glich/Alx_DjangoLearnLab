from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CustomUser
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=CustomUser)
def signal_for_token(sender, instance, created, **kwargs):
    if created:
        return Token.objects.create(user=instance)
        