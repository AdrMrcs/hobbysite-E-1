from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Profile")
    name = models.CharField(max_length=63)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f'{self.name} | {self.email}'

# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance, name=instance.username, email=instance.email)