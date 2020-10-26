from django import forms
from django.conf import settings
import tweepy

class TwitterForm(forms.Form):

    def __str__(self):
        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
        api  = tweepy.API(auth)
        query = ['textil']

    def search(self):
        return None
