from django.db import models

# Create your models here.


class Tweet(models.Model):
    consulted_at = models.DateTimeField()
    created_at = models.DateTimeField()
    userName = models.CharField(max_length=200)
    isVerified = models.BooleanField()
    userFollowers_count = models.IntegerField()
    userFriends_count = models.IntegerField()
    userFacourites_count = models.IntegerField()
    userStatuses_count = models.IntegerField()
    tweet_id = models.BigIntegerField()
    tweet = models.TextField()
    tweetRetweet_count = models.IntegerField()
    tweetFavorite_count = models.IntegerField()
    tweetLocation = models.TextField()


    # consulted_at = models.DateTimeField()
    # created_at = models.DateTimeField()
    # userName = models.CharField(max_length=200)
    # isVerified = models.BooleanField()
    # userFollowers_count = models.IntegerField()
    # userFriends_count = models.IntegerField()
    # userFacourites_count = models.IntegerField()
    # userStatuses_count = models.IntegerField()
    # tweet_id = models.BigIntegerField()
    # tweet = models.TextField()
    # tweetRetweet_count = models.IntegerField()
    # tweetFavorite_count = models.IntegerField()
    # tweetLocation = models.TextField()


