from django.db import models


# Create your models here.
class Tweet(models.Model):
    """
    Modelos para guardar los datos de twitter
    """
    consulted_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField()
    userName = models.CharField(max_length=200)
    isVerified = models.BooleanField()
    userFollowers_count = models.IntegerField()
    userFriends_count = models.IntegerField()
    userFavourites_count = models.IntegerField()
    userStatuses_count = models.IntegerField()
    tweet_id = models.BigIntegerField(primary_key=True)
    tweet = models.TextField()
    tweetRetweet_count = models.IntegerField()
    tweetFavorite_count = models.IntegerField()
    tweetLocation = models.TextField()

    def __str__(self):
        return self.tweet
