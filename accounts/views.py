import requests
from requests_oauthlib import OAuth1Session
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.conf import settings



consumer_key = settings.CONSUMER_KEY
consumer_secret = settings.CONSUMER_SECRET
access_token = settings.ACCESS_TOKEN    
token_secret = settings.TOKEN_SECRET


def getRequestToken():
    url = 'https://api.twitter.com/oauth/request_token'
    oauth = OAuth1Session(consumer_key, consumer_secret, access_token, token_secret)
    request_token = oauth.fetch_request_token(url)
    return request_token


def getAccessToken(oauth_token, oauth_verifier):
    url = 'https://api.twitter.com/oauth/access_token'
    payload = {'oauth_token': oauth_token, 'oauth_verifier': oauth_verifier}
    r = requests.post(url, params=payload, auth=(consumer_key, consumer_secret))

    result = {}
    if(r.status_code) == 200:
        r = r.text
        content = r.split('&')

        ro_oauth_token = content[0].split('=')
        result['oauth_token'] = ro_oauth_token[1]

        ro_oauth_token_secret = content[1].split('=')
        result['oauth_token_secret'] = ro_oauth_token_secret[1]

        ro_user_id = content[2].split('=')
        result['user_id'] = ro_user_id[1]

        ro_screen_name = content[3].split('=')
        result['screen_name'] = ro_screen_name[1]
    return result



def login_view(request):
    get_parameters = request.GET
    get_parameters = get_parameters.dict()

    if 'oauth_token' in get_parameters.keys():
        oauth_token = get_parameters.get('oauth_token')
        oauth_token_verifier = get_parameters.get('oauth_verifier')
        access_token = getAccessToken(oauth_token, oauth_token_verifier)
        print(access_token)
        username = access_token['screen_name']
        oauth_token = access_token['oauth_token']
        oauth_token_secret = access_token['oauth_token_secret']

        user = authenticate(oauth_token=oauth_token, oauth_token_secret=oauth_token_secret)
        
        if user is not None:
            print("User is not none")
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
        else:
            user = User(username=username)
            user.save()
            profile = Profile(user=user, oauth_token=oauth_token, oauth_token_secret=oauth_token_secret)
            profile.save()
            login(request, user)
        
        print(request.user.is_authenticated)
        return redirect('home')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def twitter_redirect(request):
    request_token = getRequestToken()
    oauth_token = request_token.get('oauth_token')
    return redirect(f'https://api.twitter.com/oauth/authenticate?oauth_token={oauth_token}')