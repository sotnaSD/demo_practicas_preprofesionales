import tweepy
from django.conf import settings


# conexion con la api de twiiter
def getAPI(request):
    # configuracion  de tokens de twitter
    oauth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    oauth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(oauth)
    return api
