from django.db import models


# Create your models here.
class ProductoOlx(models.Model):
    id_busqueda = models.IntegerField()
    id_producto = models.IntegerField()
    titulo = models.CharField(max_length=200)
    precio = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    url = models.CharField(max_length=200)
