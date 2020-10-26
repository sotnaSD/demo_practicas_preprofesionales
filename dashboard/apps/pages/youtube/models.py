from django.db import models
from django.conf import settings
# Create your models here.


class YoutubeVideo(models.Model):
    videoId = models.CharField(max_length=20)
    titulo = models.CharField(max_length=200)
    fechaPublicacion = models.DateTimeField()
    numeroVistas = models.IntegerField()
    numeroDisLikes =  models.IntegerField()
    numeroLikes = models.IntegerField()
    numeroComentarios= models.IntegerField()
