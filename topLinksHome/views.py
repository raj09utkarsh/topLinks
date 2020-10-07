from django.shortcuts import render, redirect
from requests_oauthlib import OAuth1Session
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings


consumer_key = settings.CONSUMER_KEY
consumer_secret = settings.CONSUMER_SECRET
access_token = settings.ACCESS_TOKEN
token_secret = settings.TOKEN_SECRET


def get_timeline(request):
    url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
    username = request.user.get_username()
    user = User.objects.filter(username=username).first()
    profile = Profile.objects.filter(user=user).first()
    resource_owner_key = profile.oauth_token
    resource_owner_secret = profile.oauth_token_secret

    oauth = OAuth1Session(consumer_key,
                          client_secret=consumer_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret)
    r = oauth.get(url).json()
    print(r)
    return r


@login_required(redirect_field_name='home')
def home(request):
    r = get_timeline(request)
    tweets = []
    for tweet_response in r:
        content = {}
        content['user'] = tweet_response['user']['screen_name']
        content['url'] = tweet_response['entities']['urls']
        tweets.append(content)
    
    context = {
        'tweets': tweets
    }
    
    return render(request, 'topLinksHome/home.html', context)
