from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Profile


class SettingsBackend(BaseBackend):
    def authenticate(self, request, oauth_token=None, oauth_token_secret=None):
        profile = Profile.objects.filter(oauth_token=oauth_token, oauth_token_secret=oauth_token_secret).first()
        print(profile)
        if profile is not None:
            try:
                user = User.objects.get(username=profile.user.username)
            except User.DoesNotExist:
                user = None
            return user
        return None

    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None