from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    oauth_token = models.CharField(max_length=100)
    oauth_token_secret = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username