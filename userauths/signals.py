from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

@receiver(post_save, sender=apps.get_model('userauths', 'User'))
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        create_user_profile.objects.create(user=instance)
