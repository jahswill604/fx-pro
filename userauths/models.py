from django.db import models
from core.models import *
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class User (AbstractUser):
    email = models.EmailField( unique=True)
    username = models.CharField(max_length=100)
    


   

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__ (self):
        return self.username



class UserProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    

    def __str__(self):
        return self.user.username


class Withdrawal(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} on {self.timestamp}"







@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)




