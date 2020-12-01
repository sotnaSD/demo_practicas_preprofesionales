from django.db import models


# Create your models here.
class Busqueda(models.Model):
    """
    Modelo para el historial de busqueda cuando se hace un web scraping
    """
    id_busqueda = models.IntegerField()
    texto = models.CharField(max_length=100)
    fecha = models.DateField(auto_now=True)
    n_paginas = models.IntegerField()
    sitios = models.CharField(max_length=30)


class Link(models.Model):
    """
    Modelo para los links de busqueda cuando se hace un web scraping
    """
    id_busqueda = models.IntegerField()
    id_link = models.IntegerField()
    url = models.CharField(max_length=200)
    buscador = models.CharField(max_length=50)
