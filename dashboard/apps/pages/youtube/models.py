from django.db import models
from django.conf import settings
# Create your models here.


class YoutubeVideo(models.Model):
    videoId = models.CharField(max_length=20, primary_key=True)
    titulo = models.CharField(max_length=200)
    fechaConsulta = models.CharField(max_length=20, default=None)
    fechaPublicacion = models.CharField(max_length=20)
    numeroVistas = models.IntegerField()
    numeroDisLikes =  models.IntegerField()
    numeroLikes = models.IntegerField()
    numeroComentarios= models.IntegerField()


class YoutubeComentario(models.Model):
    videoId = models.CharField(max_length=20)
    fechaConsulta = models.CharField(max_length=20, default=None)
    fechaPublicacion = models.CharField(max_length=20)
    trend = models.CharField(max_length=20)
    comentario = models.CharField(max_length=1000)
    comentarioLikes = models.IntegerField()
    comentarioRespuestas = models.IntegerField()
    isTopLevel = models.BooleanField()
